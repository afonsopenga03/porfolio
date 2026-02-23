from django.shortcuts import render, get_object_or_404
from .models import Category, Project, ProjectImage, Category
from django.utils.text import slugify
from .forms import ProjectForm, ProjectImageFormSet
from django.contrib.admin.views.decorators import staff_member_required # Importação importante

def index(request):
    category_slug = request.GET.get('category')

    if category_slug:
        projects = Project.objects.filter(category__slug=category_slug)
    else:
        projects = Project.objects.all()

    categories = Category.objects.all()

    return render(request, 'index.html', {
        'projects': projects,
        'categories': categories
    })


    
    return render(request, 'index.html', context)



"""def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)

    return render(request, 'project_detail.html', {
        'project': project
    })"""
    
def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'project_detail.html', {'project': project})
    
def sobre(request):
    return render(request, "sobre.html")

def skills(request):
    return render(request, "skills.html")

from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

# views.py
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings

def contato(request):
    if request.method == 'POST':
        nome = request.POST.get('name')
        email = request.POST.get('email')
        mensagem = request.POST.get('message')

        if nome and email and mensagem:
            try:
                send_mail(
                    f'Mensagem de {nome} - Contato do Site',
                    f'Nome: {nome}\nE-mail: {email}\n\nMensagem:\n{mensagem}',
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Mensagem enviada com sucesso!')
            except Exception as e:
                messages.error(request, f'Erro ao enviar: {e}')
        else:
            messages.error(request, 'Todos os campos são obrigatórios.')

        return redirect('contato')  # Nome da URL da página de contato

    return render(request, 'contato.html')  # Substitua pelo caminho real

def projetos(request):
    context = {
        'projects': Project.objects.all().order_by('-created_at'),
        'categories': Category.objects.all(),
    }
    return render(request, 'projetos.html', context)

"""def dashboard(request):
    if request.method == 'POST':
        # Captura os dados do formulário
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        category = Category.objects.get(id=category_id)
        
        # Cria o projeto (gerando o slug automaticamente se estiver vazio)
        project = Project.objects.create(
            title=title,
            category=category,
            slug=slugify(title) 
        )

        # Captura múltiplas imagens
        images = request.FILES.getlist('images')
        for img in images:
            ProjectImage.objects.create(project=project, image=img)
            
        return redirect('dashboard') # Recarrega a página ou vai para a lista

    categories = Category.objects.all()
    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'dashboard.html', {
        'categories': categories,
        'projects': projects
    })"""
    
@staff_member_required(login_url='admin:login')
def dashboard(request, project_id=None):
    # Se project_id existir, estamos EDITANDO, senão estamos CRIANDO
    instance = get_object_or_404(Project, id=project_id) if project_id else None
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=instance)
        formset = ProjectImageFormSet(request.POST, request.FILES, instance=instance)
        
        if form.is_valid() and formset.is_valid():
            project = form.save()
            formset.save() # O formset lida com criar, editar e DELETAR fotos
            
            action = "atualizado" if instance else "criado"
            messages.success(request, f"Projeto '{project.title}' {action} com sucesso!")
            return redirect('dashboard')
        else:
            messages.error(request, "Erro ao salvar. Verifique os campos abaixo.")
    else:
        form = ProjectForm(instance=instance)
        formset = ProjectImageFormSet(instance=instance)

    projects = Project.objects.all().order_by('-created_at')
    return render(request, 'dashboard.html', {
        'form': form,
        'formset': formset,
        'projects': projects,
        'is_editing': bool(instance),
        'project_instance': instance
    })

@staff_member_required(login_url='admin:login')
def delete_project(request, project_id):
    if request.method == 'POST':
        project = get_object_or_404(Project, id=project_id)
        project.delete()
        messages.warning(request, "Projeto removido permanentemente.")
    return redirect('dashboard')