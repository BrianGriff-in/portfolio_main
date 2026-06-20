from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_herosection_resume'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visitor_id', models.CharField(db_index=True, max_length=64)),
                ('vote_type', models.CharField(choices=[('like', 'Like'), ('dislike', 'Dislike')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('gallery_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='home.galleryitem')),
            ],
            options={
                'verbose_name': 'Gallery Vote',
                'verbose_name_plural': 'Gallery Votes',
            },
        ),
        migrations.AddConstraint(
            model_name='galleryvote',
            constraint=models.UniqueConstraint(fields=('gallery_item', 'visitor_id'), name='unique_gallery_visitor_vote'),
        ),
    ]