
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.Field import BooleanField, ObjectField, Field
from AccessControl import ClassSecurityInfo
from Products.Archetypes.Registry import registerField
from Products.Archetypes.Registry import registerWidget


class YesNoWidget(TypesWidget):
    _properties = TypesWidget._properties.copy()
    _properties.update({
        'macro' : "yesnowidget",
        'yesmsg': 'Yes',
        'nomsg': 'No'
        })

    security = ClassSecurityInfo()

class YesNoField(BooleanField):
    """A field that stores boolean values."""
    __implements__ = ObjectField.__implements__
    _properties = Field._properties.copy()
    _properties.update({
        'widget' : YesNoWidget
        })

    security  = ClassSecurityInfo()

    security.declarePrivate('set')
    def set(self, instance, value, **kwargs):
        """If value is not defined or equal to 0, set field to false;
        otherwise, set to true."""
        if value in ['0', 'False', None, False, 0, 'No']:
            value = False
        else:
            value = True

        ObjectField.set(self, instance, value, **kwargs)


registerField(YesNoField,
              title='YesNo',
              description='Used for storing boolean values but displaying as yes/no')
              
              
registerWidget(YesNoWidget,
             title='YesNo',
             description='Renders a HTML yes/no selection',
             used_for=('Products.UWOshOIE.widgets.YesNoField',)
             )
