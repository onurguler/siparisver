import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'siparisver.settings')
django.setup()


from core.models import ProductCategory, Product


# en_cok_tercih_edilenler = ProductCategory.objects.create(
#     title='En Çok Tercih Edilenler')
# menuler = ProductCategory.objects.create(title='Menüler')
et_donerler = ProductCategory.objects.create(title='Et Dönerler')
tavuk_donerler = ProductCategory.objects.create(title='Tavuk Dönerler')
yan_urunler = ProductCategory.objects.create(title='Yan Ürünler')
tatlilar = ProductCategory.objects.create(title='Tatlılar')
icecekler = ProductCategory.objects.create(title='İçecekler')
poset = ProductCategory.objects.create(title='Poşet')

# Et Dönerler
Product.objects.create(title='Et Döner Dürüm',
                       content='Domates, turşu, maydanoz ve isteğe göre soğan',
                       price=12,
                       category=et_donerler)

Product.objects.create(title='Zurna Et Döner Dürüm',
                       content='Domates, turşu, maydanoz ve isteğe göre soğan',
                       price=14,
                       category=et_donerler)

Product.objects.create(title='Somun Ekmek Arası Et Döner',
                       content='Domates, turşu, maydanoz ve isteğe göre soğan',
                       price=9,
                       category=et_donerler)

Product.objects.create(title='Et Döner',
                       content='Domates, yeşilbiber, patates kızartması',
                       price=16,
                       category=et_donerler)

Product.objects.create(title='İskender (Et Dönerden)',
                       content='Domates, yeşilbiber, yoğurt, özel sos',
                       price=19,
                       category=et_donerler)

Product.objects.create(title='Pilav Üstü Et Döner',
                       content='Domates, yeşilbiber, patates kızartması, pilav',
                       price=18,
                       category=et_donerler)

# Tavuk Dönerler

Product.objects.create(title='Tavuk Döner Dürüm',
                       content='80 gr. tavuk döner, marul, turşu, patates kızartması, özel sos, mayonez',
                       price=9,
                       category=tavuk_donerler)

Product.objects.create(title='Zurna Tavuk Döner Dürüm',
                       content='Marul, turşu, patates kızartması, özel sos, mayonez',
                       price=11,
                       category=tavuk_donerler)

Product.objects.create(title='Somun Ekmek Arası Tavuk Döner',
                       content='Marul, turşu, patates kızartması, özel sos, mayonez',
                       price=6.5,
                       category=tavuk_donerler)

Product.objects.create(title='Tavuk Döner',
                       content='Domates, yeşilbiber, patates kızartması',
                       price=14,
                       category=tavuk_donerler)

Product.objects.create(title='İskender (Tavuk Dönerden)',
                       content='Domates, yeşilbiber, yoğurt, özel sos',
                       price=16,
                       category=tavuk_donerler)

Product.objects.create(title='Pilav Üstü Tavuk Döner',
                       content='Domates, yeşilbiber, patates kızartması, pilav',
                       price=15,
                       category=tavuk_donerler)


# Yan Ürünler

Product.objects.create(title='Patates Kızartması',
                       content='',
                       price=5,
                       category=yan_urunler)

# Tatlılar

Product.objects.create(title='Sütlaç',
                       content='',
                       price=2.5,
                       category=tatlilar)

Product.objects.create(title='Keşkül',
                       content='',
                       price=2.5,
                       category=tatlilar)

Product.objects.create(title='Kazandibi',
                       content='',
                       price=2.5,
                       category=tatlilar)

Product.objects.create(title='Sakızlı Muhallebi',
                       content='',
                       price=2.5,
                       category=tatlilar)

Product.objects.create(title='Puding',
                       content='',
                       price=2.5,
                       category=tatlilar)
# İçecekler

Product.objects.create(title='Pepsi (33 cl.)',
                       content='',
                       price=4,
                       category=icecekler)

Product.objects.create(title='Pepsi Light (33 cl.)',
                       content='',
                       price=4,
                       category=icecekler)

Product.objects.create(title='Yedigün (33 cl.)',
                       content='',
                       price=4,
                       category=icecekler)

Product.objects.create(title='Lipton Ice Tea Şeftali (33 cl.)',
                       content='',
                       price=4,
                       category=icecekler)

Product.objects.create(title='Şalgam Suyu (30 cl.)',
                       content='',
                       price=2.5,
                       category=icecekler)

Product.objects.create(title='Ayran (29 cl.)',
                       content='',
                       price=2.5,
                       category=icecekler)

Product.objects.create(title='Ayran (20 cl.)',
                       content='',
                       price=1.5,
                       category=icecekler)

Product.objects.create(title='Su',
                       content='',
                       price=1,
                       category=icecekler)

Product.objects.create(title='Pepsi (1 L.)',
                       content='',
                       price=6,
                       category=icecekler)

Product.objects.create(title='Pepsi Light (1 L.)',
                       content='',
                       price=6,
                       category=icecekler)

Product.objects.create(title='Pepsi Max (1 L.)',
                       content='',
                       price=6,
                       category=icecekler)

Product.objects.create(title='Yedigün (1 L.)',
                       content='',
                       price=6,
                       category=icecekler)

Product.objects.create(title='Fruko (1 L.)',
                       content='',
                       price=6,
                       category=icecekler)

# Poşet

Product.objects.create(title='Poşet',
                       content='',
                       price=0.25,
                       category=poset)
