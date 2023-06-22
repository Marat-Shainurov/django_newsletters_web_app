from django.views import generic

from blog.models import Blog


class BlogDetailView(generic.DetailView):
    model = Blog

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Blog detail'

        self.object.views += 1
        self.object.save()

        return context
