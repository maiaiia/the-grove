from strawberry.fastapi import GraphQLRouter
from fastapi import Request, Response

class CustomGraphQLRouter(GraphQLRouter):
    async def __call__(self, request: Request, response: Response):
        result = await super().__call__(request, response)

        context = getattr(request.state, "graphql_context", None)
        if context is None:
            return result

        if "set_auth_cookie" in context:
            response.set_cookie(
                key="access_token",
                value=context["set_auth_cookie"],
                httponly=True,
                max_age=60 * 60 * 24,
                samesite="lax",
                secure=False
            )

        if context.get("clear_auth_cookie"):
            response.delete_cookie(key="access_token")

        return result