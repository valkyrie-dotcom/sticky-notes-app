# notes/tests.py
from django.test import TestCase
from django.urls import reverse

from .forms import NoteForm
from .models import Note


class NoteModelTest(TestCase):
    def setUp(self):
        # Create a Note object for testing
        self.note = Note.objects.create(
            title='Test Note', content='This is a test note.')

    def test_note_has_title(self):
        # Test that a Note object has the expected title
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.title, 'Test Note')

    def test_note_has_content(self):
        # Test that a Note object has the expected content
        note = Note.objects.get(id=self.note.id)
        self.assertEqual(note.content, 'This is a test note.')

    def test_note_string_is_title(self):
        # Test that a Note is shown by its title
        self.assertEqual(str(self.note), 'Test Note')


class NoteFormTest(TestCase):
    def test_form_is_valid_with_title_and_content(self):
        form = NoteForm(data={'title': 'A title', 'content': 'Some text'})
        self.assertTrue(form.is_valid())

    def test_form_is_invalid_without_title(self):
        form = NoteForm(data={'title': '', 'content': 'Some text'})
        self.assertFalse(form.is_valid())


class NoteViewTest(TestCase):
    def setUp(self):
        # Create a Note object for testing views
        self.note = Note.objects.create(
            title='Test Note', content='This is a test note.')

    def test_note_list_view(self):
        # Test the note-list view
        response = self.client.get(reverse('note_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')

    def test_note_detail_view(self):
        # Test the note-detail view
        response = self.client.get(
            reverse('note_detail', args=[str(self.note.id)]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Note')
        self.assertContains(response, 'This is a test note.')

    def test_note_detail_view_missing_note(self):
        # Test that a note which does not exist gives a 404
        response = self.client.get(reverse('note_detail', args=['999']))
        self.assertEqual(response.status_code, 404)

    def test_note_create_view_shows_empty_form(self):
        response = self.client.get(reverse('note_create'))
        self.assertEqual(response.status_code, 200)

    def test_note_create_view_saves_note(self):
        # Test that posting valid data creates a note and redirects
        response = self.client.post(
            reverse('note_create'),
            {'title': 'New Note', 'content': 'New content'})
        self.assertRedirects(response, reverse('note_list'))
        self.assertTrue(Note.objects.filter(title='New Note').exists())

    def test_note_create_view_rejects_missing_title(self):
        # Test that invalid data is not saved and the form is shown again
        response = self.client.post(
            reverse('note_create'), {'title': '', 'content': 'No title'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Note.objects.count(), 1)

    def test_note_update_view_changes_note(self):
        # Test that posting new data updates the existing note
        response = self.client.post(
            reverse('note_update', args=[str(self.note.id)]),
            {'title': 'Changed', 'content': 'Changed content'})
        self.assertRedirects(response, reverse('note_list'))
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Changed')
        self.assertEqual(self.note.content, 'Changed content')

    def test_note_delete_view_removes_note(self):
        # Test that deleting a note removes it from the database
        response = self.client.get(
            reverse('note_delete', args=[str(self.note.id)]))
        self.assertRedirects(response, reverse('note_list'))
        self.assertFalse(Note.objects.filter(id=self.note.id).exists())
