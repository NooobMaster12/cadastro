from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from io import BytesIO
import qrcode


# Create your models here.


class Funcionario(models.Model):
    nome = models.CharField(max_length=100)
    usuario = models.OneToOneField(User,on_delete=models.CASCADE ,related_name= 'funcionario')
    cpf = models.CharField(max_length=11)
    funcao = models.CharField(max_length=50)
    telefone = models.CharField(max_length=20)
    
    def __str__(self):
        return "{}- {}" .format(self.nome, self.funcao)
    
class Sala(models.Model):
    descricao = models.CharField(max_length=50)
    numero = models.CharField(max_length=20)

    def __str__(self):
        return "{} - {}".format(self.numero, self.descricao)


class Chave(models.Model):
    disponivel = models.BooleanField('Disponivel',default=True)
    sala = models.ForeignKey(Sala, on_delete= models.CASCADE, related_name= 'chaves')
    qr_code = models.ImageField(upload_to='qr_codes/', null=True, blank=True)

    def __str__(self):
        return "{} - {}".format(self.sala.numero, self.sala.descricao)
    
@receiver(post_save, sender=Chave)
def criar_qrcode(sender, instance, created, **kwargs):
    if created:
        sala_numero = instance.id
        qr_code = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr_code.add_data(sala_numero)
        qr_code.make(fit=True)

        qr_code_image = qr_code.make_image()

        stream = BytesIO()
        qr_code_image.save(stream, "PNG")
        instance.qr_code.save(f'{instance.sala.numero}.png', stream)
    
    
    
    
class Aluguel(models.Model):
    usuario = models.ForeignKey(Funcionario, on_delete=models.DO_NOTHING, related_name='usuario_alugueis')
    chave = models.ForeignKey(Chave, on_delete=models.DO_NOTHING, related_name='alugueis') 
    data_aluguel = models.DateTimeField(auto_now_add=True)
    data_devolucao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "{} - {} - {}".format(self.usuario.nome, self.chave.sala.descricao, self.data_aluguel)
    
    
    class Meta:
        verbose_name = "Aluguel"
        verbose_name_plural = "Alugueis"