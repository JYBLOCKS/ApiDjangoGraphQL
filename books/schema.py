from email import message
import graphene
from graphene_django import DjangoObjectType
from .models import Books


class BooksType(DjangoObjectType):
    class Meta:
        model = Books
        fields = ("id", "title", "excerpt")


class Query(graphene.ObjectType):
    all_books = graphene.List(BooksType)

    def resolve_all_books(root, info):
        return Books.objects.all()

# save a new book


class BookSave(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        excerpt = graphene.String(required=True)

    ok = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, title, excerpt):
        try:
            book = Books(title=title, excerpt=excerpt)
            book.save()
            ok = True
            message = "Save new Book"
        except:
            ok = False
            message = "Can't Save Book"

        return BookSave(ok=ok, message=message)

# update a book


class BookUpdate(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String(required=True)
        excerpt = graphene.String(required=True)

    ok = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, id, title, excerpt):
        try:
            book = Books.objects.get(id=id)
            book.title = title
            book.excerpt = excerpt
            book.save()
            ok = True
            message = "Update new Book with id = " + id
        except:
            ok = False
            message = "Can't Update Book"

        return BookUpdate(ok=ok, message=message)

# delete a book


class BookDelete(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()
    message = graphene.String()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            book = Books.objects.get(id=id)
            book.delete()
            ok = True
            message = "Delete Book with id = " + id
        except:
            ok = False
            message = "Can't Delete Book"

        return BookDelete(ok=ok, message=message)

# expression of mutation a book


class Mutation(graphene.ObjectType):
    save_book = BookSave.Field()
    update_book = BookUpdate.Field()
    delete_book = BookDelete.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
