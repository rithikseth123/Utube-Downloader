from django.views.generic import View
from pytube import YouTube
from django.shortcuts import render, redirect
from django.http import HttpResponse
import os


class home(View):
    def __init__(self, url=None):
        self.url = url

    def get(self, request):
        return render(request, "utubedownloader/index.html")

    def post(self, request):
        # for fetching the video
        if request.POST.get("fetch-vid"):
            self.url = request.POST.get("given_url")
            video = YouTube(self.url)
            vidTitle, vidThumbnail = video.title, video.thumbnail_url
            qual, stream = [], []
            for vid in video.streams.filter(progressive=True):
                qual.append(vid.resolution)
                stream.append(vid)
            context = {
                "vidTitle": vidTitle,
                "vidThumbnail": vidThumbnail,
                "qual": qual,
                "stream": stream,
                "url": self.url,
            }
            return render(request, "utubedownloader/index.html", context)

        # for downloading the video
        elif request.POST.get("download-vid"):
            self.url = request.POST.get("given_url")
            video = YouTube(self.url)
            video_qual = video.streams[int(request.POST.get("download-vid")) - 1]
            video_file = video_qual.download()

            # Get the file name
            file_name = os.path.basename(video_file)

            # Open the file and serve it as a response
            with open(video_file, "rb") as file:
                response = HttpResponse(file.read(), content_type="video/mp4")
                response["Content-Disposition"] = f'attachment; filename="{file_name}"'
                return response

        return render(request, "utubedownloader/index.html")
