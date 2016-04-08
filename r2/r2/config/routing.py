# The contents of this file are subject to the Common Public Attribution
# License Version 1.0. (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://code.reddit.com/LICENSE. The License is based on the Mozilla Public
# License Version 1.1, but Sections 14 and 15 have been added to cover use of
# software over a computer network and provide for limited attribution for the
# Original Developer. In addition, Exhibit A has been modified to be consistent
# with Exhibit B.
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for
# the specific language governing rights and limitations under the License.
#
# The Original Code is reddit.
#
# The Original Developer is the Initial Developer.  The Initial Developer of
# the Original Code is reddit Inc.
#
# All portions of the code written by reddit are Copyright (c) 2006-2015 reddit
# Inc. All Rights Reserved.
###############################################################################

"""
Setup your Routes options here
"""
from routes import Mapper


def not_in_sr(environ, results):
    return ('subreddit' not in environ and
            'sub_domain' not in environ and
            'domain' not in environ)


# FIXME: submappers with path prefixes are broken in Routes 1.11. Once we
# upgrade, we should be able to replace this ugliness with submappers.
def partial_connect(mc, **override_args):
    def connect(path, **kwargs):
        if 'path_prefix' in override_args:
            path = override_args['path_prefix'] + path
        kwargs.update(override_args)
        mc(path, **kwargs)
    return connect


def make_map(config):
    map = Mapper(explicit=False)
    map.minimization = True
    mc = map.connect

    # Username-relative userpage redirects, need to be defined here in case
    # a plugin defines a `/user/:name` handler.

    for plugin in reversed(config['r2.plugins']):
        plugin.add_routes(mc)

    mc('/robots.txt', controller='robots', action='robots')
    mc('/crossdomain', controller='robots', action='crossdomain')

    mc('/', controller='forms', action='login')
    mc('/logout', controller='forms', action='logout')
    mc('/adminon', controller='forms', action='adminon')
    mc('/adminoff', controller='forms', action='adminoff')
    mc('/admin/errors', controller='errorlog')

    mc("/gtm/jail", controller="googletagmanager", action="jail")
    mc("/gtm", controller="googletagmanager", action="gtm")

    mc('/post/:action/:url_user', controller='post',
       requirements=dict(action="login"))
    mc('/post/:action', controller='post',
       requirements=dict(action="login"))

    mc('/api/:action/:url_user', controller='api',
       requirements=dict(action="login"))

    mc('/api/server_seconds_visibility', controller='api',
       action='server_seconds_visibility')

    mc('/code', controller='redirect', action='redirect',
       dest='http://github.com/reddit/')

    # Used for showing ads
    mc("/ads/", controller="ad", action="ad")

    mc("/try", controller="forms", action="try_compact")

    mc("/web/timings", controller="weblog", action="timings")

    mc("/web/log/:level", controller="weblog", action="message",
       requirements=dict(level="error"))

    mc("/web/poisoning", controller="weblog", action="report_cache_poisoning")

    # This route handles displaying the error page and
    # graphics used in the 404/500
    # error pages. It should likely stay at the top
    # to ensure that the error page is
    # displayed properly.
    mc('/error/document/:id', controller='error', action="document")

    # these should be near the buttom, because they should only kick
    # in if everything else fails. It's the attempted catch-all
    # reddit.com/http://... and reddit.com/34fr
    mc("/*url", controller='front', action='catchall')

    return map
