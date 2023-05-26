from django.shortcuts import render, redirect
import openai
import os
# Create your views here.
from django.http import HttpResponse

# openai.api_key = os.environ['GPTPATH']
# openai.api_key = "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"
openai.api_key = os.environ["GPTPATH"]
def search(request):
    if request.POST:
        place = request.POST["pref_id"]
        period = request.POST["day"]
        trans = request.POST["trans"]
        get_date = ','.join(request.POST["date"].split("-"))
        date = get_date[0] + "年" + get_date[1] + "月" + get_date[2] + "日"
        interests = request.POST.getlist("interests")
        rule = """
        あなたは旅行ガイドです。Userからの質問に以下のルールに従って答えてください。
        ルール
        1. 今から旅行プランを考えていただきますが，以下の形式に従って回答してください。
        1日目
        時刻 : 場所-説明時刻
        時刻 : 場所-説明
        ...
        2日目
        時刻 : 場所-説明
        時刻 : 場所-説明
        ...
        
        2. 1で示した形式に必要ない文章は省いてください。以下のような文章は必要ありません。
        ~のプランを提案します。
        以上が，~のプランです。
        """

        text = f"""
        以下の条件に合わせた旅行プランを考えてください。
        日程：{date}
        日数：{period}
        交通手段:{trans}
        場所：{place}
        ジャンル:{interests}
        日程はあくまで季節を考慮したもので，返答に日程を書く必要はありません。ルールは必ず守ってください。
        """
        
        period + "を" + trans + "で" + place + "の旅行プラン"
        messages = []
        messages.append({"role": "system", "content": rule})
        messages.append({"role": "user", "content": text})
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )

        # results = response["choices"][0]["message"]["content"].split("\n")
        context = {
            "results" : response["choices"][0]["message"]["content"].split("\n")
        }
        # return render(request, "tourplan/results.html", context)
        return render(request, "tourplan/results.html", context)


    return render(request, "tourplan/index.html")
