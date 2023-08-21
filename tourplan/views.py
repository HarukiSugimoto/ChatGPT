from django.shortcuts import render, redirect
import openai
import os
# Create your views here.
from django.http import HttpResponse

openai.api_key = os.environ["GPTPATH"]
def search(request):
    if request.POST:
        place = request.POST["pref_id"]
        period = request.POST["day"]
        trans = request.POST["trans"]
        get_date = request.POST["date"].split("-")
        date = get_date[0] + "年" + get_date[1] + "月" + get_date[2] + "日"
        interests = request.POST.getlist("interests")
        keywords = request.POST["key"]
        text = f"""
        以下の条件に合わせた旅行プランを考え，先ほど示した命令書に100%必ず従え。余計な文章は必ず省け。
        日程：{date}
        日数：{period}
        交通手段:{trans}
        場所：{place}
        ジャンル:{" ".join(interests)}
        キーワード:{keywords}
        """

        rule = """
        #命令書:
        あなたはプロの旅行ガイドです。
        以下の制約と条件をもとに，最高の旅行プランを提案してください。

        #制約条件:
        ・日程：
            日程はあくまでも季節を考慮するためのものである。
        ・日数：
            日帰りや1泊2日など指定された条件で考える必要がある。1泊2日であれば1日目と2日目を考える。2泊3日であれば1日目, 2日目, 3日目を考える。
        ・交通手段:
            指定された交通手段で旅行プランを考える。
        ・場所：
            指定された場所の旅行プランを考える。
        ・ジャンル:
            指定されたジャンルを含めた旅行プランを考える。指定されなければ特に考えなくて良い。
        ・キーワード:
            指定されたキーワードを含めた旅行プランを考える。指定されなければ特に考えなくて良い。

        #出力フォーマット: 
            1日目\n
            00:00 : 場所-説明\n
            滞在時間 : n分\n
            移動:交通手段-n分\n
            00:00 : 場所-説明\n
            滞在時間 : n分\n
            ...
            移動:交通手段-n分\n
            00:00 : 場所-説明\n
            滞在時間 : n分\n
            
            2日目\n
            00:00 : 場所-説明\n
            滞在時間 : n分\n
            移動:交通手段-n分\n
            00:00 : 場所-説明\n
            滞在時間 : n分\n
            ...
            移動:交通手段-n分\n
            00:00 : 場所-説明\n
            滞在時間 : n分\n
        
        #注意
        ・日数が日帰りと指定された場合は出力フォーマットの"1日目"のところを"日帰り"にかえろ。
        ・日数が1泊2日の場合は1日目と2日目，2泊3日の場合は1日目と2日目と3日目を考えろ。その他も同様。
        ・一度行った場所はなるだけ他の日で行かないようにしてください。再訪は禁止。
        """
        
        messages_pre = []
        messages_pre.append({"role": "system", "content": rule})
        messages_pre.append({"role": "user", "content": text})
        response_pre = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages_pre,
        )
        results = response_pre["choices"][0]["message"]["content"]
        context = {
            "results" : results.split("\n")
        }
        print(results)
        # return render(request, "tourplan/results.html", context)
        return render(request, "tourplan/results.html", context)


    return render(request, "tourplan/index.html")
