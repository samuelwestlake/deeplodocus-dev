from aiohttp import web


from deeplodocus.ui.views import index



class Routes(object):


    def __init__(self):
        self.list_routes = self.__load_routes()

    def setup_routes(self, app):
        """
        Authors : Alix Leroy,
        Add the routes to the app
        :param app: The app to which we add the routes
        :return: None
        """
        for route in self.list_routes:
            app.router.add_route(route[0], route[1], route[2], name=route[3])


    def __load_routes(self):
        """
        Authors : Alix Leroy,
        Load in memory the list of routes
        :return: The list of routes
        """

        routes = [
            ('GET', '/', index, 'homepage')
        ]


        return routes