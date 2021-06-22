from subprocess import Popen, PIPE, STDOUT


pl = Popen(['coral-cli', 'login', '-d', 'comments.genexist.com'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
pl.stdout.readline()
pl.stdin.write('it@straitsinteractive.com'.encode())
pl.stdin.write('1234qwer'.encode())
pl.stdin.flush()
pl.stdout.readline()

import pexpect
child = pexpect.spawn('coral-cli story:update -d comments.genexist.com --id=DIS-2LSuHdx6VavKMjKoUZcobm --url=https://www.dpexnetwork.org/discussions/forum/compliance-with-regulations/LRn6dzRAKP/topic/contact-tracing-retention-of-visitor-data/2LSuHdx6VavKMjKoUZcobm/')
child.expect('coral: Enter your login credentials')
child.expect('Email: ')
child.sendline('it@straitsinteractive.com')
child.expect('Password: ')
child.sendline('1234qwer')
child.expect(pexpect.EOF)



pl = Popen(['coral-cli', 'story:update', '-d', 'comments.genexist.com', '--id=DIS-2LSuHdx6VavKMjKoUZcobm', '--url=https://www.dpexnetwork.org/discussions/forum/ciance-with-regulations/LRn6dzRAKP/topic/contact-tracing-retention-of-visitor-data/2LSuHdx6VavKMjKoUZcobm/'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
pl.stdin.write('it@straitsinteractive.com'.encode())
pl.stdin.write('1234qwer'.encode())
pl.stdin.write('yes'.encode())


coral-cli story:update -d comments.genexist.com --id=DIS-2LSuHdx6VavKMjKoUZcobm --url=https://www.dpexnetwork.org/discussions/forum/compliance-with-regulations/LRn6dzRAKP/topic/contact-tracing-retention-of-visitor-data/2LSuHdx6VavKMjKoUZcobm/

pout = p.communicate(input='yes'.encode())[0]





https://www.dpexnetwork.org/discussions/forum/ciance-with-regulations/LRn6dzRAKP/topic/contact-tracing-retention-of-visitor-data/2LSuHdx6VavKMjKoUZcobm/

