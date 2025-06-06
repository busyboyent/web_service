from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ParsedPage
from .serializers import ParsedPageSerializer
from .utils import parse_page


class ParsedPageViewSet(viewsets.ModelViewSet):
    queryset = ParsedPage.objects.all()
    serializer_class = ParsedPageSerializer

    @action(detail=False, methods=['post'])
    def create_page(self, request):
        """
        Post /page/create
        :param request:
        :return:
        """
        url = request.data.get('url')
        if not url:
            return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)

        parsed_data = parse_page(url)
        if 'error' in parsed_data:
            return Response({'error': parsed_data['error']}, status=status.HTTP_400_BAD_REQUEST)

        page = ParsedPage.objects.create(url=url, **parsed_data)

        # есть легкое ощущение, что неправильно разрешать записывать в базу записи с одинаковым url
        # подумать над тем, чтобы обновлять существующую запись в базе, если сслыка уже существует
        return Response({'id': page.id}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def get_page(self, request, pk=None):
        """
        GET page/object_id
        :param request:
        :param pk:
        :return:
        """
        page = self.get_object()
        serializer = self.get_serializer(page)

        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def list_pages(self, request):
        """
        GET /page/list
        GET /page/list?order=hN
        GET /page/list?order=-hN
        :param request:
        :return:
        """
        order = request.query_params.get('order', None)
        queryset = self.get_queryset()

        if order and order not in ['h1', 'h2', 'h3', '-h1', '-h2', '-h3']:
            return Response(
                {'error': 'Invalid order parameter. Use h1, h2, h3 with optional - prefix'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # в задании требуется обратная сортировка относительно синтаксиса order_by
        # полагаю, что не очень круто будет делать .reverse() для очень большой записи поэтому поправим название поля
        if order:
            order = order.lstrip('-') if order.startswith('-') else f'-{order}'

        queryset = queryset.order_by(order if order else '-created_at')
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
