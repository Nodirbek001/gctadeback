import os
from pathlib import Path

from apps.product.models import Order
import pandas as pd
import requests


def bot_send_message(order_id, message):
    token = "6138093434:AAH4QgpH-svw8Q8F3MLW5k0oEeyHYJyznT8"
    channel_id = "-1001600409662"
    if order_id:
        order = Order.objects.get(id=order_id)
        # create excel file

        excel_file_path = create_order_excel(order)

        # send excel file
        files = {"document": open(excel_file_path, "rb")}
        url = f"https://api.telegram.org/bot{token}/sendDocument"
        params = {"chat_id": channel_id, "caption": message}
        requests.post(url, data=params, files=files)
        os.remove(excel_file_path)


def create_order_excel(order):
    cart_items = order.cart.items.all()

    order_data = {
        "ID zakaz": [order.pk],
        "Status": [order.get_status_display()],
        "Name": [order.name],
        "Phone": [order.phone],
        "Date": [order.created_at.strftime("%Y-%m-%d %H:%M")],
        "Summa": [order.cart.total_price]
    }
    cart_data = {
        "Product": [cart_item.product.title for cart_item in cart_items],
        "Price": [cart_item.product.price for cart_item in cart_items],
        "Count": [cart_item.quantity for cart_item in cart_items],
        "Summa": [cart_item.product.price * cart_item.quantity for cart_item in cart_items]
    }

    # Create DataFarm

    order_df = pd.DataFrame(order_data)
    cart_df = pd.DataFrame(cart_data)
    excel_file_path = Path(__file__).resolve().parent.parent.parent / f"order_{order.pk}.xlsx"
    with pd.ExcelWriter(excel_file_path, engine="openpyxl") as writer:
        order_df.to_excel(writer, sheet_name="zakaz", index=False)
        cart_df.to_excel(writer, sheet_name="cart", index=False)

        # Iterator
        for sheet in writer.sheets.values():
            for column in sheet.columns:
                max_length = 0
                column = [cell for cell in column]
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except TypeError:
                        pass
                adjusted_width = (max_length + 2) * 1.2
                sheet.column_dimensions[column[0].column_letter].width = adjusted_width
    return excel_file_path
str