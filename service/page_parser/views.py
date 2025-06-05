from django.shortcuts import render
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
            h1_count=parsed_data['h1_count'],
            h2_count=parsed_data['h2_count'],
            h3_count=parsed_data['h3_count'],
            links=parsed_data['links']
        )

        return Response({'id': page.id}, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def get_page(self, request, pk=None):
        page = self.get_object()
        data = {
            'h1': page.h1_count,
            'h2': page.h2_count,
            'h3': page.h3_count,
            'a': page.links
        }
        return Response(data)

    @action(detail=False, methods=['get'])
    def list_pages(self, request):
        order = request.query_params.get('order', None)
        queryset = self.get_queryset()

        if order:
            # Преобразуем h1, h2, h3 в h1_count, h2_count, h3_count
            field_map = {
                'h1': 'h1_count',
                'h2': 'h2_count',
                'h3': 'h3_count',
                '-h1': '-h1_count',
                '-h2': '-h2_count',
                '-h3': '-h3_count'
            }

            if order not in field_map:
                return Response(
                    {'error': 'Invalid order parameter. Use h1, h2, h3 with optional - prefix'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            order_field = field_map[order]
            queryset = queryset.order_by(order_field)
        else:
            queryset = queryset.order_by('-created_at')

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

def create_page_view(request):
    return render(request, 'page_parser/create_page.html')
