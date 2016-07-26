
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"

home = HomeView.as_view()

class ChartsView(TemplateView):
    template_name = "charts.html"

home = HomeView.as_view()

charts = ChartsView.as_view()