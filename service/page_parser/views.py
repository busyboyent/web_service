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
        url = request.data.get('url')
        if not url:
            return Response({'error': 'URL is required'}, status=status.HTTP_400_BAD_REQUEST)

        parsed_data = parse_page(url)
        if 'error' in parsed_data:
            return Response({'error': parsed_data['error']}, status=status.HTTP_400_BAD_REQUEST)

        page = ParsedPage.objects.create(
            url=url,
            h1=parsed_data['h1'],
            h2=parsed_data['h2'],
            h3=parsed_data['h3'],
            a=parsed_data['a']
        )

        return Response({'id': page.id}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def get_page(self, request, pk=None):
        page = self.get_object()
        serializer = self.get_serializer(page)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def list_pages(self, request):
        order = request.query_params.get('order', None)
        queryset = self.get_queryset()

        if order:
            if order.lstrip('-') not in ['h1', 'h2', 'h3']:
                return Response(
                    {'error': 'Invalid order parameter. Use h1, h2, h3 with optional - prefix'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            queryset = queryset.order_by(order)
        else:
            queryset = queryset.order_by('-created_at')

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
