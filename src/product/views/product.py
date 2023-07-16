from django.views import generic
from django.views.generic.edit import UpdateView
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Prefetch
from django.urls import reverse_lazy

from product.forms import ProductForm, VariantForm, ProductImageForm, ProductVariantPriceForm
from product.models import ProductVariant, Variant, Product, ProductImage, ProductVariantPrice




class CreateProductView(generic.TemplateView):
    template_name = 'products/create.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['products'] = []
        context['variants'] = list(variants.all())
        return context

    def post(self, request, *args, **kwargs):
        title = request.POST.get('title')
        sku = request.POST.get('sku')
        description = request.POST.get('description')
        variant_forms = []
        image_forms = []
        price_forms = []

        product = Product.objects.create(title=title, sku=sku, description=description)

        for key, value in request.POST.items():
            if key.startswith('variant_title_'):
                variant_id = key.split('_')[-1]
                variant = Variant.objects.get(id=variant_id)
                variant_title = value
                variant_form = ProductVariant(variant_title=variant_title, variant=variant, product=product)
                variant_forms.append(variant_form)

            elif key.startswith('file_path_'):
                product_image = value
                image_form = ProductImage(product=product, file_path=product_image, thumbnail=0)
                image_forms.append(image_form)

            elif key.startswith('price_'):
                product_variant_id = key.split('_')[-1]
                product_variant = ProductVariant.objects.get(id=product_variant_id)
                price = value
                stock = request.POST.get(f'stock_{product_variant_id}')
                price_form = ProductVariantPrice(
                    product_variant_one=product_variant, price=price, stock=stock, product=product
                )
                price_forms.append(price_form)

        ProductVariant.objects.bulk_create(variant_forms)
        ProductImage.objects.bulk_create(image_forms)
        ProductVariantPrice.objects.bulk_create(price_forms)

        return redirect('product:product_list')
    

class UpdateProductView(UpdateView):
    template_name = 'products/create.html'
    model = Product
    form_class = VariantForm
    success_url = reverse_lazy('product:product_list')

    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        variants = Variant.objects.filter(active=True).values('id', 'title')
        context['variants'] = list(variants.all())
    
        product_instance = self.get_object()
    
        form = self.form_class(instance=product_instance)
    
        context['form'] = form
        return context


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    variants = ProductVariant.objects.filter(product=product)
    variant_prices = ProductVariantPrice.objects.filter(product=product)

    context = {
        'products': [product],
        'variants': variants,
        'variant_prices': variant_prices,
    }

    return render(request, 'products/list.html', context)

class EditProductView(generic.TemplateView):
    template_name = 'products/edit.html'


class ProductListView(generic.ListView):
    template_name = 'products/list.html'
    context_object_name = 'product_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = Product.objects.all().prefetch_related(
            Prefetch('variants', queryset=ProductVariant.objects.select_related('variant'))
        )

        title = self.request.GET.get('title')
        variant = self.request.GET.get('variant')
        price_from = self.request.GET.get('price_from')
        price_to = self.request.GET.get('price_to')
        date = self.request.GET.get('date')

        if title:
            queryset = queryset.filter(title__icontains=title)

        if variant:
            queryset = queryset.filter(variants__variant__title__icontains=variant)

        if price_from:
            queryset = queryset.filter(variants__productvariantprice__price__gte=price_from)

        if price_to:
            queryset = queryset.filter(variants__productvariantprice__price__lte=price_to)

        if date:
            queryset = queryset.filter(created_at__date=date)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_list = context['product_list']
        paginator = Paginator(product_list, self.paginate_by)
        page = self.request.GET.get('page')
        products = paginator.get_page(page)

        product_variants = []

        for product in products:
            variants = product.variants.all().select_related('variant')
            product_variants.append({
                'variant': variants[0].variant if variants else None,
                'product_variants': variants
            })

        context['products'] = products
        context['total_products'] = paginator.count
        context['variants'] = product_variants
        return context