

from rest_framework import serializers
from .models import Invoice, Product
from typing import List, Union


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"

    def validate_product_ids(self, product_ids: List[Union[int, str]], user):
        """
        Compruebo si se recibo al menos un producto.
        """
        if len(product_ids) < 1:
            raise serializers.ValidationError(
                "At least one product is required on the invoice")
        product_ids = [pk if isinstance(pk, int) else int(pk)
                       for pk in product_ids]

        existing_products = Product.objects.filter(
            pk__in=product_ids, user_id=user.id)
        existing_product_ids = [product.id for product in existing_products]

        non_existing_product_ids = set(product_ids) - set(existing_product_ids)

        if non_existing_product_ids:
            serializers.ValidationError(
                "Multiple product IDs do not exist in the database.")
        return product_ids
