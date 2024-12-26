from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST, require_GET
from .forms import PubDatasetForm
from django.contrib.auth import get_user_model
from .models import Dataset, DatasetsCategory, DatasetComment
from django.db.models import Q
from django.http import HttpResponse, Http404
from urllib.parse import quote
from django.contrib import messages
import os

User = get_user_model()


# Create your views here.

def index(request):
    categories = DatasetsCategory.objects.filter(dataset__isnull=False).distinct()
    datasets_grouped_by_category = {}
    for category in categories:
        datasets_grouped_by_category[category] = Dataset.objects.filter(category=category)
    # datasets = Dataset.objects.all()
    return render(request, "index.html", context={
        "datasets_grouped_by_category": datasets_grouped_by_category
    })


def dataset_details(request, dataset_id):
    try:
        dataset = Dataset.objects.get(pk=dataset_id)
    except Exception as e:
        dataset = None
    return render(request, "dataset_detail.html", context={'dataset': dataset})


@login_required()
def download_dataset_file(request, dataset_id):
    try:
        dataset = Dataset.objects.get(pk=dataset_id)
        file_path = dataset.file.path
        file_name = quote(dataset.file.name.split('/')[-1])
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/octet-stream')
            response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
            return response
    except Dataset.DoesNotExist:
        raise Http404("Dataset does not exist")
    except Exception as e:
        raise Http404("Error: %s" % str(e))


@require_http_methods(['GET', 'POST'])
@login_required()
def pub_dataset(request):
    if request.method == 'GET':
        categories = DatasetsCategory.objects.all()
        return render(request, "pub_dataset.html", context={'categories': categories})
    else:
        form = PubDatasetForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            content = form.cleaned_data.get('content')
            category_id = form.cleaned_data.get('category')
            file = form.cleaned_data.get('file')
            dataset = Dataset.objects.create(
                name=name,
                content=content,
                category_id=category_id,
                author=request.user,
                file=file
            )
            return JsonResponse({'code': 200,
                                 'message': "你的数据集发布成功！",
                                 'data': {"dataset_id": dataset.id}})
        else:
            print(form.errors)
            return JsonResponse({"code": 400, "message": "表单验证错误！"})


@require_POST
@login_required()
def pub_comment(request):
    dataset_id = request.POST.get('dataset_id')
    content = request.POST.get('content')
    DatasetComment.objects.create(content=content, dataset_id=dataset_id, author=request.user)
    # 在发布评论后，刷新界面，重新导向到这个界面
    return redirect(reverse("sharingPlatform:dataset_details",
                            kwargs={'dataset_id': dataset_id}))


@require_GET
def search(request):
    # 查找的形式为 search/?q=xxx
    q = request.GET.get('q')
    # 从数据集的标题和内容中查找包含关键字的信息
    categories = DatasetsCategory.objects.filter(dataset__isnull=False).distinct()
    datasets_grouped_by_category = {}
    for category in categories:
        datasets_grouped_by_category[category] = Dataset.objects.filter(
            Q(category=category) & (Q(name__icontains=q) | Q(content__icontains=q)))
    # datasets = Dataset.objects.filter(Q(name__icontains=q) | Q(content__icontains=q)).all()
    return render(request, 'index.html', context={
        'datasets_grouped_by_category': datasets_grouped_by_category
    })


@require_GET
def search_myself(request):
    categories = DatasetsCategory.objects.filter(dataset__isnull=False).distinct()
    datasets_grouped_by_category = {}
    for category in categories:
        datasets_grouped_by_category[category] = Dataset.objects.filter(
            Q(category=category) & Q(author_id=request.user.id))
    # datasets = Dataset.objects.all()
    return render(request, "my_databases.html", context={
        "datasets_grouped_by_category": datasets_grouped_by_category
    })


@login_required()
def dataset_delete(request, dataset_id):
    try:
        dataset = Dataset.objects.get(pk=dataset_id)
        # 获取文件路径
        file_path = dataset.file.path
        # 删除数据库记录
        dataset.delete()
        # 删除文件
        if os.path.exists(file_path):
            os.remove(file_path)
        messages.success(request, "数据集已成功删除。")
        return redirect(reverse("sharingPlatform:index"))
    except Dataset.DoesNotExist:
        messages.error(request, "数据集不存在。")
        return redirect(reverse("sharingPlatform:index"))
    except Exception as e:
        messages.error(request, f"删除数据集时出错: {str(e)}")
        return redirect(reverse("sharingPlatform:index"))


@login_required()
def edit_dataset(request, dataset_id):
    dataset = get_object_or_404(Dataset, id=dataset_id)

    if request.method == 'POST':
        form = PubDatasetForm(request.POST, request.FILES or None)
        if not request.FILES.get('file'):
            form.fields['file'].required = False

        if form.is_valid():
            dataset.name = form.cleaned_data['name']
            dataset.content = form.cleaned_data['content']
            dataset.category_id = form.cleaned_data['category']
            if 'file' in request.FILES:
                if dataset.file and os.path.isfile(dataset.file.path):
                    os.remove(dataset.file.path)
                dataset.file = request.FILES['file']
            dataset.save()
            return JsonResponse({'code': 200,
                                 'message': "你的数据集修改成功！",
                                 'data': {"dataset_id": dataset.id}})
        else:
            print(form.errors)
            return JsonResponse({"code": 400, "message": "表单验证错误！"})
    return render(request, 'edit_dataset.html', {
        # 'form': form,
        'categories': DatasetsCategory.objects.all(),
        'dataset': dataset
    })
