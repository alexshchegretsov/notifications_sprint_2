from aiohttp import web

from dramatiq_tasks import sort


async def index(request):
    post_data = await request.json()
    if not post_data.get('event'):
        raise web.HTTPBadRequest(text='Event not found')

    sort.send(post_data)
    return web.HTTPAccepted(text='Accepted')
