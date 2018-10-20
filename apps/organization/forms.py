__author__ = "GodSuperK"
__date__ = "18-10-20 上午9:33"

import re
from django import forms

from operation.models import UserAsk


class UserAskModelForm(forms.ModelForm):
    """
    ModelForm 可以继承 模型的字段，同时也可以新增字段
    """

    class Meta:
        model = UserAsk
        fields = ['name', 'phone', 'course_name']

    def clean_phone(self):
        """正则：手机号（精确）,验证手机号是否合法

        移动：134(0-8)、135、136、137、138、139、147、150、151、152、157、158、159、178、182、183、184、187、188、198
        联通：130、131、132、145、155、156、175、176、185、186、166
        电信：133、153、173、177、180、181、189、199
        全球星：1349
        虚拟运营商：170
        :return:
        """
        phone = self.cleaned_data["phone"]
        REGEX_PHONE_EXACT = "^((13[0-9])|(14[5,7])|(15[0-3,5-9])|(17[0,3,5-8])|(18[0-9])|166|198|199|(147))\\d{8}$"
        # 将正则表达式编译为pattern对象
        pattern = re.compile(REGEX_PHONE_EXACT)
        # 验证用户输入的手机号是否符合我们的 pattern 规则
        if pattern.match(phone):
            return phone
        # 不符合规则，抛出 forms.ValidationError 异常
        else:
            raise forms.ValidationError(message="手机号码非法", code="phone_invalid")
