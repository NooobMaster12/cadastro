from django.db import models
from django.contrib.auth.models import User

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

    
@receiver(post_save, sender=Chave)
def criar_qrcode(sender, instance, created, **kwargs):
    if created:
        qr_code = generate_qrcode(instance.codigo)
        instance.qr_code.save(f'{instance.id}.png', qr_code)
    def __str__(self):
        return '{} - {}'.format(self.disponivel, self.sala.descricao)
    
    
    
    
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