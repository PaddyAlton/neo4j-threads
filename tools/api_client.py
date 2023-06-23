# tools/api_client.py
# make it easy to send some test API requests

from requests import delete, get, post

HOST = "http://localhost:8765"


# convenience functions
def get_all_(path: str):
    return get(f"{HOST}/{path}")


def get_all_threads():
    return get_all_("thread").json()


def get_all_users():
    return get_all_("user").json()


def get_thread(id: str):
    return get(f"{HOST}/thread/{id}").json()


def get_reply(id: str):
    thread_id = "dummy"
    return get(f"{HOST}/thread/{thread_id}/reply/{id}").json()


def create_user(user_name: str):
    resp = post(f"{HOST}/user", json={"name": user_name})
    return resp.json()


def create_thread(user_id: str, title: str, body: str):
    params = {"user_id": user_id}
    resp = post(f"{HOST}/thread", json={"title": title, "body": body}, params=params)
    return resp.json()


def create_top_level_reply(user_id: str, thread_id: str, body: str):
    params = {"user_id": user_id}
    resp = post(f"{HOST}/thread/{thread_id}/reply", json={"body": body}, params=params)
    return resp.json()


def create_nested_reply(user_id: str, reply_id: str, body: str):
    params = {"user_id": user_id}
    thread_id = "dummy"
    resp = post(
        f"{HOST}/thread/{thread_id}/reply/{reply_id}",
        json={"body": body},
        params=params,
    )
    return resp.json()


def upvote_a_thread(user_id: str, thread_id: str, reverse: bool = False):
    method = delete if reverse else post
    params = {"user_id": user_id}
    resp = method(f"{HOST}/thread/{thread_id}/upvote", params=params)
    return resp.json()


def upvote_a_reply(user_id: str, reply_id: str, reverse: bool = False):
    method = delete if reverse else post
    params = {"user_id": user_id}
    thread_id = "dummy"
    resp = method(f"{HOST}/thread/{thread_id}/reply/{reply_id}/upvote", params=params)
    return resp.json()


def downvote_a_reply(user_id: str, reply_id: str, reverse: bool = False):
    method = delete if reverse else post
    params = {"user_id": user_id}
    thread_id = "dummy"
    resp = method(f"{HOST}/thread/{thread_id}/reply/{reply_id}/downvote", params=params)
    return resp.json()


### test runs
def test_run_1():
    users = get_all_users()
    the_user = users[1]["uuid"]
    r = create_thread(the_user, "How about this Kant guy?", "See title.")
    print(r)


def test_run_2():
    bessie = create_user("Bessie")
    threads = get_all_threads()
    r = create_top_level_reply(
        bessie["uuid"],
        threads[0]["uuid"],
        "I am fine, as it happens. Thanks for asking!",
    )
    print(r)


def test_run_3():
    threads = get_all_threads()
    the_thread = get_thread(threads[0]["uuid"])
    the_reply = get_reply(the_thread["children"][-1]["uuid"])
    end_of_thread = the_reply["children"][-1]["uuid"]
    users = get_all_users()
    r = create_nested_reply(users[1]["uuid"], end_of_thread, "I'm 100% confident.")
    print(r)


def test_run_4():
    threads = get_all_threads()
    the_thread = get_thread(threads[0]["uuid"])
    top_level_reply = get_reply(the_thread["children"][-1]["uuid"])
    end_of_thread = top_level_reply["children"][-1]["uuid"]
    users = get_all_users()
    immanuel = users[2]["uuid"]
    r1 = upvote_a_thread(immanuel, the_thread["uuid"])
    print(r1)
    r2 = downvote_a_reply(immanuel, top_level_reply["uuid"])
    print(r2)
    r3 = upvote_a_reply(users[2]["uuid"], end_of_thread)
    print(r3)


