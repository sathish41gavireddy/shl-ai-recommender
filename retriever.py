import json


with open("catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)




def search_assessments(query):

    query = query.lower()

    results = []

    keywords = query.split()

    for item in catalog:

        searchable_text = " ".join([
            str(item.get("name", "")),
            str(item.get("description", "")),
            str(item.get("keys", "")),
            str(item.get("job_levels", "")),
            str(item.get("languages", "")),
            str(item.get("duration", "")),
        ]).lower()

        score = 0

        for word in keywords:
            if word in searchable_text:
                score += 1

        if score > 0:
            results.append((score, item))

 
    results.sort(key=lambda x: x[0], reverse=True)

    return [item for score, item in results[:10]]




def filter_remote(assessments):

    remote_tests = []

    for item in assessments:

        if item.get("remote", "").lower() == "yes":

            remote_tests.append(item)

    return remote_tests




def compare_assessments(name1, name2):

    test1 = None
    test2 = None

    for item in catalog:

        if name1.lower() in item.get("name", "").lower():
            test1 = item

        if name2.lower() in item.get("name", "").lower():
            test2 = item

    return test1, test2



def get_assessment(name):

    for item in catalog:

        if name.lower() in item.get("name", "").lower():
            return item

    return None