from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.
class Game(models.Model):
    name = models.CharField(max_length=128,unique=True)
    users = models.ManyToManyField(User)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def save(self,*args,**kwargs):
        self.slug = slugify(self.name)
        super(Game, self).save(*args, **kwargs)

        scores_this = Score.objects.all().filter(game=self)
        scored_users = map(lambda x: x.user,scores_this)
        print('here')
        for user in self.users.all():
            Score.objects.get_or_create(game=self,user=user)

    @property
    def rows(self):
        return Row.objects.filter(game=self).order_by('created_at')

    def get_score_for_user(self,user):
        return Score.objects.get(user=user,game=self).value
        


class Score(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{str(self.game)}:{self.user}'

    @property
    def value(self):
        columns = Column.objects.all().filter(user=self.user)
        return sum(column.value for column in columns if column.row in self.game.rows)


class Row(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    game = models.ForeignKey(Game,on_delete=models.CASCADE)

    def save(self,*args,**kwargs):
        super(Row, self).save(*args, **kwargs)

        this_game = Game.objects.get(id=self.game.id)
        users = this_game.users.all()
        for user in users:
            c ,_ = Column.objects.get_or_create(row=self,user=user)
            c.save()

    def save_no_cols(self,*args,**kwargs):
        super(Row, self).save(*args, **kwargs)


    @property
    def columns(self):
        return Column.objects.all().filter(row=self).order_by('user__id')

    def __str__(self):
        return f'{self.game}:{self.created_at}'

class Column(models.Model):
    row = models.ForeignKey(Row,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    value = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.user}:{self.value}'


