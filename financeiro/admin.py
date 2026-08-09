from django.contrib import admin

from .models import MovimentacaoFinanceira


@admin.register(MovimentacaoFinanceira)
class MovimentacaoFinanceiraAdmin(admin.ModelAdmin):

    list_display = (

        "categoria",

        "tipo",

        "valor",

        "status",

        "data",

    )

    list_filter = (

        "tipo",

        "status",

        "forma_pagamento",

    )

    search_fields = (

        "categoria",

        "observacao",

    )