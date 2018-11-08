from aiohttp import web

import aiohttp_jinja2


@aiohttp_jinja2.template('test.html')
async def index(request):
    return {'name': 'Andrew',
            'surname': 'Svetlov'}