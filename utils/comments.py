import requests

from django.conf import settings

def update_story(story_id, story_url):
    mutation_update_query = """
        mutation($story: UpdateStoryInput!) {
            updateStory(input: $story) {
                    story {
                        id,
                        url
                    }
                }
            }
    """
    variables = """
        {{
            "story" : {{
                "id": "{story_id}",
                "clientMutationId": "{story_id}",
                "story": {{
                    "url": "{story_url}"
                }}
            }}
        }}
    """.format(story_id=story_id, story_url='https://www.dpexnetwork.org' + story_url)
    headers = {
        'Authorization': 'Bearer {}'.format(settings.COMMENT_APP_TOKEN)
    }
    response = requests.post('https://comments.genexist.com/api/graphql/',
                             json={
                                 'query': mutation_update_query,
                                 'variables': variables,
                             },
                             headers=headers
                             )
    errors = response.json().get('errors')
    if errors:
        raise Exception('Can not update story: {}'.format(errors))
    return True
