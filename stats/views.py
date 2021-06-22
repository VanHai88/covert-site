import random

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.utils.dateparse import parse_date

from collections import Counter, OrderedDict
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta

from .models import CountColor

@login_required
def user_stats(request):
    if not request.user.is_staff:
        return redirect('/')

    ylist = []
    year = date.today().year

    while year >= 2020:
        ylist.append(year)
        year -= 1
    
    ylist.reverse()

    template = "user_stats.html"

    span = "%s - %s" % (datetime.now() - timedelta(days=60), datetime.now())
    template_vars = {'span':span, 'ylist':ylist}
    return render(request, template, template_vars)


@login_required
def ajax_user_stats(request):
    colors = CountColor.objects.all()
    color_dict = {str(obj.country): obj.color for obj in colors}

    if request.method == 'POST':
        cyear = date.today().year
        year = int(request.POST.get('year', 0))
        span = request.POST.get('span')

        if year:
            if cyear == year:
                drange = ['%s-01-01' % year, str(date.today())]
            else:
                drange = ['%s-01-01' % year, '%s-12-31' % year ]
        else:
            drange = request.POST.get('range').split(' - ')

        query  = Q(date_joined__gte=drange[0]) & Q(date_joined__lte=drange[1])
        users = list(User.objects.filter(query).prefetch_related('uprofile').order_by('date_joined'))

        crange = []
        start = parse_date(drange[0])
        cdate = start
        end  = parse_date(drange[1])
        days = (end - start).days

        if year and span != 'month':
            crange.append(cdate)
            cdate += timedelta(days=(7 - cdate.weekday()))

        while cdate < end:
            crange.append(cdate)
            if year:
                if span == 'month':
                    cdate += relativedelta(months=1)
                else:
                    cdate += timedelta(days=14)

            else:
                cdate += timedelta(days=1)

        crange.append(end)

        country_list = []

        uidx = 0
        udict = OrderedDict()

        for i, xdate in enumerate(crange[1:]):
            ccounter = Counter()
            for u in users[uidx:]:
                if u.date_joined.date() < xdate:
                    try:
                        cty = str(u.uprofile.country)
                        if cty not in country_list:
                            country_list.append(cty)
                        ccounter[cty] += 1
                    except:
                        pass
                    uidx += 1 
                else:
                    break
            
            
            prev = crange[i] 
            dnext = xdate - timedelta(days=1)
            udict['%s/%s - %s/%s' % (prev.day, prev.month, dnext.day, dnext.month)] = ccounter

        labels = list(udict.keys())


        country_dict = {}
        for x in country_list:
            color = color_dict.get(x, '#000')
            vals = [val[x] for val in udict.values()]
            country_dict[x] = {'color':color, 'values': vals}

        template = "__ajax_user_stats.html"
        template_vars = {'country_dict':country_dict, 'labels':labels}
        return render(request, template, template_vars)