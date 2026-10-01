import csv
import io

from django import forms
from django.http import HttpResponse
from django.shortcuts import redirect, render


class CSVUploadForm(forms.Form):
    arquivo = forms.FileField(label="Arquivo CSV")


def csv_download_response(filename, headers, row):
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(headers)
    writer.writerow(row)
    response = HttpResponse(buffer.getvalue(), content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def render_csv_upload(admin_instance, request, title, download_url, importer):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = form.cleaned_data["arquivo"]
            if not arquivo.name.lower().endswith(".csv"):
                form.add_error("arquivo", "Envie um arquivo com extensão .csv.")
            else:
                try:
                    resultado = importer(arquivo)
                    mensagem = ", ".join(f"{quantidade} {chave}" for chave, quantidade in resultado.items())
                    admin_instance.message_user(request, f"Importação concluída: {mensagem}.")
                    return redirect("..")
                except Exception as exc:
                    form.add_error(None, str(exc))
    else:
        form = CSVUploadForm()

    context = {
        **admin_instance.admin_site.each_context(request),
        "title": title,
        "form": form,
        "download_url": download_url,
        "opts": admin_instance.model._meta,
    }
    return render(request, "admin/import_csv.html", context)
