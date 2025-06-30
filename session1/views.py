from rest_framework.views import APIView
from rest_framework.views import Response

class Home(APIView):
    def get(self, request):
        return Response({'name': 'Ohayio!'})
    def post(self, request):
        data = request.data.get("name")
        print(data)
        return Response(data)
    

