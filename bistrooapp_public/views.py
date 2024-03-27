from datetime import datetime
from django.shortcuts import render
from bistrooapp_admin.models import Menuu, Theme

def show_menu(request):
    menu_date = datetime.today()
    q_result_menuu = (Menuu.objects.filter(menu_date=menu_date).
                      values("category_name__category_name", "description", "price_full", "price_half", "is_hided"))
    q_result_theme = Theme.objects.filter(menu_date=menu_date)
    formatted_date = menu_date.strftime("%d.%m.%Y")

    if q_result_menuu or q_result_theme:
        is_menuu = True
    else:
        is_menuu = False

    for item in q_result_menuu:
        if str(item["price_full"]) > "0.00" and (str(item["price_half"]) > "0.00" and str(item["price_half"]) != "None"):
            item["price_full"] = str(item["price_full"]) + " / " + str(item["price_half"])
        elif ((str(item["price_full"]) == "0.00" and str(item["price_half"]) == "0.00") or
                (str(item["price_full"]) == "0.00" and str(item["price_half"]) == "None")):
            item["price_full"] = "Prae hinna sees"

    context = {
        "formatted_date": formatted_date,
        "is_menuu": is_menuu,
        "menuu_items": q_result_menuu,
        "themes": q_result_theme,
    }
    return render(request, "bistrooapp_public/index.html", context)
