from flask.wrappers import Response


def successful():
    return Response(
        "Success", 200
    )


def unsupported():
    return Response(
        "Unsupported media type", 415
    )


def unauthorised():
    return Response(
        "Unauthorised", 401
    )
