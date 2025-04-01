from django.db import models
from django.contrib.auth.models import User
# Organización


class Organization(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    nit = models.CharField(max_length=20, unique=True)
    contact_info = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

# Clausula


class Clause(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title

# Tipo de Identificación


class TypeIdentification(models.Model):
    abbreviation = models.CharField(max_length=10)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.description

# Usuario extendido


class ExtendedUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    identification_number = models.CharField(max_length=20, unique=True)
    birth_date = models.DateField()
    address = models.TextField()
    type_identification = models.ForeignKey(
        TypeIdentification, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

# Tipos de Contrato


class TypeContract(models.Model):
    type_contract = models.CharField(max_length=100)

    def __str__(self):
        return self.type_contract

# Áreas


class Area(models.Model):
    name_area = models.CharField(max_length=255)

    def __str__(self):
        return self.name_area

# Puestos


class Post(models.Model):
    name_posts = models.CharField(max_length=255)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return self.name_posts

# Contratos


class Contract(models.Model):
    STATUS_CHOICES = [
        ('PENDIENTE', 'Pendiente'),
        ('EN CURSO', 'En Curso'),
        ('POR FINALIZAR', 'Por Finalizar'),
        ('FINALIZADO', 'Finalizado'),
    ]
    APPROVAL_CHOICES = [
        ('APROBADO', 'Aprobado'),
        ('EN ESPERA', 'En Espera'),
        ('DESAPROBADO', 'Desaprobado'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    type_contract = models.ForeignKey(TypeContract, on_delete=models.CASCADE)
    approval = models.CharField(
        max_length=20, choices=APPROVAL_CHOICES, default='EN ESPERA')
    start_date = models.DateField()
    end_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='PENDIENTE')

    def __str__(self):
        return f"{self.user.username} - {self.status}"

# Clausulas de contrato


class ContractClause(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title
