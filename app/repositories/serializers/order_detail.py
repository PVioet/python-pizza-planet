from app.plugins import ma
from .beverage import BeverageSerializer
from .ingredient import IngredientSerializer
from ..models import OrderDetail


class OrderDetailSerializer(ma.SQLAlchemyAutoSchema):

    ingredient = ma.Nested(IngredientSerializer)
    beverage = ma.Nested(BeverageSerializer)

    class Meta:
        model = OrderDetail
        load_instance = True
        fields = (
            'price',
            'ingredient',
            'beverage',
        )
