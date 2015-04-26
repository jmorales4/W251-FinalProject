import os
import web
import object_storage
import json

render_video = web.template.render('templates/').video
render_videos = web.template.render('templates/').content_list

# A class to build the latest videos UI
class page:
    # the GET route
    def GET(self):
        # Read the 'person' parameter that may have been submitted with request
        input = web.input()
        person = input.person if input.has_key('person') else ''

        # Get the latest videos
        videopath = '/static/gifs/' + person
        try:
            videos = sorted(os.listdir(videopath))

            video_html = ''
            for i, video in enumerate(videos):
                video_html = video_html + str(render_video(i, videopath + '/' + video))

        except Exception as e:
            print e
            return 0, '<p>{0}</p>'.format(e)

            # And render the results via templates/videos.html
        return render_videos(person, video_html)



