# from django.conf import settings

# class categories():
#     def __init__(self):
#         self.category = category

#     def add_categories(self, request):
#         for cat in request:
#             if cat['id'] not in self.category:
#                 self.category[cat['id']] = {
#                     "nome" : cat["nome"],
#                     "idcategoriapai" : cat["idcategoriapai],
#                     "campos" : cat["campos"]
#                 }