import aiosql
from transformers import pipeline
from wordcloud import STOPWORDS
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import base64
import math
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
import re
from tmdb_utils import get_recommendations
import json
import requests
from omdb_utils import get_motion_picture_info
from scraping_utils import extract_tagline
from tmdb_utils import get_actor_profile_picture

queries = aiosql.from_path("sql", "psycopg2")

def extract_and_insert_reviews(conn, motion_picture_id, title, type):
    driver = webdriver.Chrome()
    driver.get("https://www.imdb.com/")
    search_box = driver.find_element(By.NAME, "q")
    search_box.send_keys(f"{title}")
    search_box.send_keys(Keys.RETURN)

    home_url = driver.find_element(By.CLASS_NAME, "ipc-metadata-list-summary-item__t").get_attribute("href")
    home_url = home_url.split("?")[0]
    driver.get(f"{home_url}reviews?ref_=tt_urv")

    cnt = 0
    while cnt < 7:
        try:
            button = driver.find_element(By.CLASS_NAME, "ipl-load-more__button")
            button.click()
            time.sleep(4)
            cnt += 1
        except:
            break
    
    complete_reviews = driver.find_elements(By.CLASS_NAME, "lister-item-content")
    for complete_review in complete_reviews:
        date = complete_review.find_element(By.CLASS_NAME, "review-date").text
        title = complete_review.find_element(By.CLASS_NAME, "title").text
        try:
            rating = complete_review.find_element(By.CLASS_NAME, "rating-other-user-rating").text[:-3]
        except:
            rating = 0
        try:
            review = complete_review.find_element(By.CLASS_NAME, "content").text
        except:
            review = ""

        if review == "":
            continue
        review = review.replace("\n", "")
        review = review.replace("\\'", "'")
        pattern = "\d+ out of \d+ found this helpful. Was this review helpful"
        removed_text = re.sub(pattern, "", review)
        pattern = "Sign in to vote."
        removed_text = re.sub(pattern, "", removed_text)
        pattern = "Permalink"
        removed_text = re.sub(pattern, "", removed_text)
        review = str(removed_text)
        date = date.split()
        day = date[0]
        month = date[1]
        year = date[2]
        if len(day) == 1:
            day = '0' + day
        if month == 'January':
            month = '01'
        elif month == 'February':
            month = '02'
        elif month == 'March':
            month = '03'
        elif month == 'April':
            month = '04'
        elif month == 'May':
            month = '05'
        elif month == 'June':
            month = '06'
        elif month == 'July':
            month = '07'
        elif month == 'August':
            month = '08'
        elif month == 'September':
            month = '09'
        elif month == 'October':
            month = '10'
        elif month == 'November':
            month = '11'
        elif month == 'December':
            month = '12'

        date = year + '-' + month + '-' + day
        queries.insert_review(conn, motion_picture_id=motion_picture_id, title=title, rating=int(rating), review=review, review_date=date)

def get_all_details(conn, id1, mtype):
    if mtype == 1:
        motion_picture_info = queries.get_movie_by_id(conn, id=id1)
    elif mtype == 2:
        motion_picture_info = queries.get_show_by_id(conn, id=id1)

    genres_info = queries.get_genres_by_motion_picture_id(conn, id=id1)
    actors_info = queries.get_actors_by_motion_picture_id(conn, id=id1)
    writers_info = queries.get_writers_by_motion_picture_id(conn, id=id1)
    movie_dict = {
        "id": motion_picture_info[0],
        "title": motion_picture_info[1],
        "poster": motion_picture_info[2],
        "tagline": motion_picture_info[3],
        "desc": motion_picture_info[4],
    }
    if mtype == 1:
        movie_dict["director"] = motion_picture_info[5]
    genres = []
    for genre in genres_info:
        genres.append(genre[1])
    movie_dict["genres"] = genres
    writers = []
    for writer in writers_info:
        writers.append(writer[1])
    movie_dict["writers"] = writers
    actors = []
    for actor in actors_info:
        actor_dict = {
            "name": actor[1],
            "profilePicture": actor[2]
        }
        actors.append(actor_dict)
    movie_dict["actors"] = actors
    reviews = []
    reviews_info = queries.get_review_by_id(conn, motion_picture_id=motion_picture_info[0])
    for review in reviews_info[:5]:
        likes = queries.get_likes(conn, review_id=review[0])
        dislikes = queries.get_dislikes(conn, review_id=review[0])
        review_dict = {
            "id": review[0],
            "title": review[3],
            "text": review[5],
            "rating": review[4],
            "date": review[6],
            "likes": likes,
            "dislikes": dislikes
        }
        reviews.append(review_dict)
    movie_dict["reviews"] = reviews

    # Summarization model
    summarization_model = pipeline(model="ainize/bart-base-cnn", max_length=1024)
    review_data = []
    for review in reviews_info[:3]:
        review_data.append(review[5])
    concat_reviews = " ".join(review_data)
    summary = summarization_model(concat_reviews)[0]["summary_text"]
    movie_dict["summary"] = summary
    

    stop_words = ["want", "many", "literally", "much", "want", "series", "yet", "happened",
                "everyone", "Mr", "sure", "upon", "getting", "ride", "Perharps", "thing",
                "wanted"] + list(STOPWORDS)
    stop_words = stop_words + ["0o", "0s", "3a", "3b", "3d", "6b", "6o", "a", "a1", "a2", "a3", "a4", "ab", "able", "about", "above", "abst", "ac", "accordance", "according", "accordingly", "across", "act", "actually", "ad", "added", "adj", "ae", "af", "affected", "affecting", "affects", "after", "afterwards", "ag", "again", "against", "ah", "ain", "ain't", "aj", "al", "all", "allow", "allows", "almost", "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount", "an", "and", "announce", "another", "any", "anybody", "anyhow", "anymore", "anyone", "anything", "anyway", "anyways", "anywhere", "ao", "ap", "apart", "apparently", "appear", "appreciate", "appropriate", "approximately", "ar", "are", "aren", "arent", "aren't", "arise", "around", "as", "a's", "aside", "ask", "asking", "associated", "at", "au", "auth", "av", "available", "aw", "away", "awfully", "ax", "ay", "az", "b", "b1", "b2", "b3", "ba", "back", "bc", "bd", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand", "begin", "beginning", "beginnings", "begins", "behind", "being", "believe", "below", "beside", "besides", "best", "better", "between", "beyond", "bi", "bill", "biol", "bj", "bk", "bl", "bn", "both", "bottom", "bp", "br", "brief", "briefly", "bs", "bt", "bu", "but", "bx", "by", "c", "c1", "c2", "c3", "ca", "call", "came", "can", "cannot", "cant", "can't", "cause", "causes", "cc", "cd", "ce", "certain", "certainly", "cf", "cg", "ch", "changes", "ci", "cit", "cj", "cl",
                            "clearly", "cm", "c'mon", "cn", "co", "com", "come", "comes", "con", "concerning", "consequently", "consider", "considering", "contain", "containing", "contains", "corresponding", "could", "couldn", "couldnt", "couldn't", "course", "cp", "cq", "cr", "cry", "cs", "c's", "ct", "cu", "currently", "cv", "cx", "cy", "cz", "d", "d2", "da", "date", "dc", "dd", "de", "definitely", "describe", "described", "despite", "detail", "df", "di", "did", "didn", "didn't", "different", "dj", "dk", "dl", "do", "does", "doesn", "doesn't", "doing", "don", "done", "don't", "down", "downwards", "dp", "dr", "ds", "dt", "du", "due", "during", "dx", "dy", "e", "e2", "e3", "ea", "each", "ec", "ed", "edu", "ee", "ef", "effect", "eg", "ei", "eight", "eighty", "either", "ej", "el", "eleven", "else", "elsewhere", "em", "empty", "en", "end", "ending", "enough", "entirely", "eo", "ep", "eq", "er", "es", "especially", "est", "et", "et-al", "etc", "eu", "ev", "even", "ever", "every", "everybody", "everyone", "everything", "everywhere", "ex", "exactly", "example", "except", "ey", "f", "f2", "fa", "far", "fc", "few", "ff", "fi", "fifteen", "fifth", "fify", "fill", "find", "fire", "first", "five", "fix", "fj", "fl", "fn", "fo", "followed", "following", "follows", "for", "former", "formerly", "forth", "forty", "found", "four", "fr", "from", "front", "fs", "ft", "fu", "full", "further", "furthermore", "fy", "g", "ga", "gave", "ge", "get", "gets", "getting", "gi", "give", "given", "gives", "giving", "gj", "gl", "go", "goes", "going",
                            "gone", "got", "gotten", "gr", "greetings", "gs", "gy", "h", "h2", "h3", "had", "hadn", "hadn't", "happens", "hardly", "has", "hasn", "hasnt", "hasn't", "have", "haven", "haven't", "having", "he", "hed", "he'd", "he'll", "hello", "help", "hence", "her", "here", "hereafter", "hereby", "herein", "heres", "here's", "hereupon", "hers", "herself", "hes", "he's", "hh", "hi", "hid", "him", "himself", "his", "hither", "hj", "ho", "home", "hopefully", "how", "howbeit", "however", "how's", "hr", "hs", "http", "hu", "hundred", "hy", "i", "i2", "i3", "i4", "i6", "i7", "i8", "ia", "ib", "ibid", "ic", "id", "i'd", "ie", "if", "ig", "ignored", "ih", "ii", "ij", "il", "i'll", "im", "i'm", "immediate", "immediately", "importance", "important", "in", "inasmuch", "inc", "indeed", "index", "indicate", "indicated", "indicates", "information", "inner", "insofar", "instead", "interest", "into", "invention", "inward", "io", "ip", "iq", "ir", "is", "isn", "isn't", "it", "itd", "it'd", "it'll", "its", "it's", "itself", "iv", "i've", "ix", "iy", "iz", "j", "jj", "jr", "js", "jt", "ju", "just", "k", "ke", "keep", "keeps", "kept", "kg", "kj", "km", "know", "known", "knows", "ko", "l", "l2", "la", "largely", "last", "lately", "later", "latter", "latterly", "lb", "lc", "le", "least", "les", "less", "lest", "let", "lets", "let's", "lf", "like", "liked", "likely", "line", "little", "lj", "ll", "ll", "ln", "lo", "look", "looking", "looks", "los", "lr", "ls", "lt", "ltd", "m", "m2", "ma", "made", "mainly", "make", "makes", "many",
                            "may", "maybe", "me", "mean", "means", "meantime", "meanwhile", "merely", "mg", "might", "mightn", "mightn't", "mill", "million", "mine", "miss", "ml", "mn", "mo", "more", "moreover", "most", "mostly", "move", "mr", "mrs", "ms", "mt", "mu", "much", "mug", "must", "mustn", "mustn't", "my", "myself", "n", "n2", "na", "name", "namely", "nay", "nc", "nd", "ne", "near", "nearly", "necessarily", "necessary", "need", "needn", "needn't", "needs", "neither", "never", "nevertheless", "new", "next", "ng", "ni", "nine", "ninety", "nj", "nl", "nn", "no", "nobody", "non", "none", "nonetheless", "noone", "nor", "normally", "nos", "not", "noted", "nothing", "novel", "now", "nowhere", "nr", "ns", "nt", "ny", "o", "oa", "ob", "obtain", "obtained", "obviously", "oc", "od", "of", "off", "often", "og", "oh", "oi", "oj", "ok", "okay", "ol", "old", "om", "omitted", "on", "once", "one", "ones", "only", "onto", "oo", "op", "oq", "or", "ord", "os", "ot", "other", "others", "otherwise", "ou", "ought", "our", "ours", "ourselves", "out", "outside", "over", "overall", "ow", "owing", "own", "ox", "oz", "p", "p1", "p2", "p3", "page", "pagecount", "pages", "par", "part", "particular", "particularly", "pas", "past", "pc", "pd", "pe", "per", "perhaps", "pf", "ph", "pi", "pj", "pk", "pl", "placed", "please", "plus", "pm", "pn", "po", "poorly", "possible", "possibly", "potentially", "pp", "pq", "pr", "predominantly", "present", "presumably", "previously", "primarily", "probably", "promptly", "proud", "provides", "ps", "pt", "pu", "put", "py", "q", "qj", "qu", "que", "quickly", "quite", "qv", "r", "r2", "ra", "ran", "rather", "rc", "rd", "re", "readily", "really", "reasonably", "recent", "recently", "ref", "refs", "regarding", "regardless", "regards", "related", "relatively", "research", "research-articl", "respectively", "resulted", "resulting", "results", "rf", "rh", "ri", "right", "rj", "rl", "rm", "rn", "ro", "rq", "rr", "rs", "rt", "ru", "run", "rv", "ry", "s", "s2", "sa", "said", "same", "saw", "say", "saying", "says", "sc", "sd", "se", "sec", "second", "secondly", "section", "see", "seeing", "seem", "seemed", "seeming", "seems", "seen", "self", "selves", "sensible", "sent", "serious", "seriously", "seven", "several", "sf", "shall", "shan", "shan't", "she", "shed", "she'd", "she'll", "shes", "she's", "should", "shouldn", "shouldn't", "should've", "show", "showed", "shown", "showns", "shows", "si", "side", "significant", "significantly", "similar", "similarly", "since", "sincere", "six", "sixty", "sj", "sl", "slightly", "sm", "sn", "so", "some", "somebody", "somehow", "someone", "somethan", "something", "sometime", "sometimes", "somewhat", "somewhere", "soon", "sorry", "sp", "specifically", "specified", "specify", "specifying", "sq", "sr", "ss", "st", "still", "stop", "strongly", "sub", "substantially", "successfully", "such", "sufficiently", "suggest", "sup", "sure", "sy", "system", "sz", "t", "t1", "t2", "t3", "take", "taken", "taking", "tb", "tc", "td", "te", "tell", "ten", "tends", "tf", "th", "than", "thank", "thanks", "thanx", "that", "that'll", "thats", "that's", "that've", "the", "their", "theirs", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "thered", "therefore", "therein", "there'll", "thereof", "therere", "theres", "there's", "thereto", "thereupon", "there've", "these", "they", "theyd", "they'd", "they'll", "theyre", "they're", "they've", "thickv", "thin", "think", "third", "this", "thorough", "thoroughly", "those", "thou", "though", "thoughh", "thousand", "three", "throug", "through", "throughout", "thru", "thus", "ti", "til", "tip", "tj", "tl", "tm", "tn", "to", "together", "too", "took", "top", "toward", "towards", "tp", "tq", "tr", "tried", "tries", "truly", "try", "trying", "ts", "t's", "tt", "tv", "twelve", "twenty", "twice", "two", "tx", "u", "u201d", "ue", "ui", "uj", "uk", "um", "un", "under", "unfortunately", "unless", "unlike", "unlikely", "until", "unto", "uo", "up", "upon", "ups", "ur", "us", "use", "used", "useful", "usefully", "usefulness", "uses", "using", "usually", "ut", "v", "va", "value", "various", "vd", "ve", "ve", "very", "via", "viz", "vj", "vo", "vol", "vols", "volumtype", "vq", "vs", "vt", "vu", "w", "wa", "want", "wants", "was", "wasn", "wasnt", "wasn't", "way", "we", "wed", "we'd", "welcome", "well", "we'll", "well-b", "went", "were", "we're", "weren", "werent", "weren't", "we've", "what", "whatever", "what'll", "whats", "what's", "when", "whence", "whenever", "when's", "where", "whereafter", "whereas", "whereby", "wherein", "wheres", "where's", "whereupon", "wherever", "whether", "which", "while", "whim", "whither", "who", "whod", "whoever", "whole", "who'll", "whom",
                            "whomever", "whos", "who's", "whose", "why", "why's", "wi", "widely", "will", "willing", "wish", "with", "within", "without", "wo", "won", "wonder", "wont", "won't", "words", "world", "would", "wouldn", "wouldnt", "wouldn't", "www", "x", "x1", "x2", "x3", "xf", "xi", "xj", "xk", "xl", "xn", "xo", "xs", "xt", "xv", "xx", "y", "y2", "yes", "yet", "yj", "yl", "you", "youd", "you'd", "you'll", "your", "youre", "you're", "yours", "yourself", "yourselves", "you've", "yr", "ys", "yt", "z", "zero", "zi", "zz",]
    stop_words = stop_words + ["episode", "character", ""]

    positive_reviews = []
    for review in reviews_info:
        if review[4] >= 7:
            positive_reviews.append(review[5])
    positive_wordcloud = WordCloud(max_font_size=50, max_words=100, background_color="white", stopwords = stop_words).generate(str(positive_reviews))

    plt.figure()
    plt.imshow(positive_wordcloud, interpolation="bilinear")
    # plt.title("Positive Tweets - Wordcloud")
    plt.axis("off")
    plt.savefig("positive_wordcloud.png")
    plt.close()
    with open('positive_wordcloud.png', 'rb') as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    movie_dict["wordcloud"] = image_base64
    
    sorted_reviews = queries.get_review_by_id_sorted(conn, motion_picture_id=motion_picture_info[0])

    # Calculate running average over time
    running_average = []
    running_sum = 0
    for review in sorted_reviews:
        running_sum += review[0]
        running_average.append(running_sum / (len(running_average) + 1))
    
    plt.figure()
    plt.plot(running_average)
    plt.ylabel("Overall Rating")
    plt.xticks([])
    plt.savefig("running_average.png")
    plt.close()
    with open('running_average.png', 'rb') as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode('utf-8')
    movie_dict["runningAverage"] = image_base64
    movie_dict["overallRating"] = round(running_average[-1], 2)

    number_of_recs = queries.check_recommendation_exists(conn, motion_picture_id=motion_picture_info[0])
    if number_of_recs == 0:
        if mtype == 1:
            recommendations = get_recommendations(motion_picture_info[6], mtype)
        elif mtype == 2:
            recommendations = get_recommendations(motion_picture_info[5], mtype)
        for title in recommendations:
            print(title)
            rec_id = queries.get_generic_motion_picture_id(conn, title=title)
            if rec_id is not None:
                queries.insert_recommendation(conn, motion_picture_id=motion_picture_info[0], recommended_motion_picture_id=rec_id)
            else:
                print("aa")
                new_motion_picture_info = get_motion_picture_info(title)
                if "Error" in new_motion_picture_info.keys():
                    return {"Result": "Failure"}
                new_motion_picture_info["tagline"] = extract_tagline(title)
                if new_motion_picture_info["type"] == 0:
                    motion_picture_id = queries.get_motion_picture_id(conn, title=new_motion_picture_info["title"], mtype=1)
                    if motion_picture_id is not None:
                        return {"Result": "Failure"}
                    motion_picture_id = queries.insert_movie(
                        conn,
                        title=new_motion_picture_info["title"],
                        tagline=new_motion_picture_info["tagline"],
                        description=new_motion_picture_info["description"],
                        poster=new_motion_picture_info["poster"],
                        director=new_motion_picture_info["director"],
                        tmdb_id=new_motion_picture_info["tmdb_id"]
                    )
                elif new_motion_picture_info["type"] == 1:
                    motion_picture_id = queries.get_motion_picture_id(conn, title=new_motion_picture_info["title"], mtype=2)
                    if motion_picture_id is not None:
                        return {"Result": "Failure"}
                    motion_picture_id = queries.insert_show(
                        conn,
                        title=new_motion_picture_info["title"],
                        tagline=new_motion_picture_info["tagline"],
                        description=new_motion_picture_info["description"],
                        poster=new_motion_picture_info["poster"],
                        tmdb_id=new_motion_picture_info["tmdb_id"]
                    )
                time.sleep(1)
                for actor in new_motion_picture_info["actors"].split(", "):
                    actor_profile_picture = get_actor_profile_picture(actor)
                    actor_id = queries.get_actor_id(conn, name=actor)
                    if actor_id is None:
                        actor_id = queries.insert_actor(conn, name=actor, profile_picture=actor_profile_picture)
                    queries.insert_motion_picture_actor(conn, motion_picture_id=motion_picture_id, actor_id=actor_id)
                time.sleep(1)
                for writer in new_motion_picture_info["writers"].split(", "):
                    writer_id = queries.get_writer_id(conn, name=writer)
                    if writer_id is None:
                        writer_id = queries.insert_writer(conn, name=writer)
                    queries.insert_motion_picture_writer(conn, motion_picture_id=motion_picture_id, writer_id=writer_id)
                time.sleep(1)
                for genre in new_motion_picture_info["genres"].split(", "):
                    genre_id = queries.get_genre_id(conn, name=genre)
                    if genre_id is None:
                        genre_id = queries.insert_genre(conn, name=genre)
                    queries.insert_motion_picture_genre(conn, motion_picture_id=motion_picture_id, genre_id=genre_id)
                
                extract_and_insert_reviews(conn, motion_picture_id, new_motion_picture_info["title"], new_motion_picture_info["type"])
                conn.commit()
                queries.insert_recommendation(conn, motion_picture_id=motion_picture_info[0], recommended_motion_picture_id=motion_picture_id)
    else:
        pass
    conn.commit()

    recommendations = queries.get_recommendations_by_motion_picture_id(conn, id=motion_picture_info[0])
    recommended_movies = []
    for recommendation in recommendations:
        recommendation_dict = {
            "id": recommendation[0],
            "title": recommendation[1],
            "poster": recommendation[2],
            "tagline": recommendation[3]
        }
        recommended_movies.append(recommendation_dict)
    movie_dict["recommendations"] = recommended_movies

    return movie_dict
