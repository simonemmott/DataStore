from unittest import TestCase
import logging
import json
from datastore import DataStore
from datastore.exception import NotAManagedType
from testing.reference_types import Type1, Type2
import os.path
import os

logger = logging.getLogger(__name__)
            
            
class DataStoreTests(TestCase):
    
    def test_open_data_store(self):
        ds = DataStore('testing/data/open_data_store')
        self.assertIsNotNone(ds)
        
    def test_open_data_store_raises_FileNotFound(self):
        with self.assertRaisesRegex(FileNotFoundError, "The root of the data store: 'testing/data/does_not_exist' does not exist"):
            ds = DataStore('testing/data/does_not_exist')
        with self.assertRaisesRegex(FileNotFoundError, "The root of the data store: 'testing/data/xxx' is not a directory"):
            ds = DataStore('testing/data/xxx')
        
    def test_get_reference_types(self):
        ds = DataStore('testing/data/reference_types')
        self.assertEqual(2, len(ds.types()))
        self.assertTrue('Type1' in ds.types())
        self.assertTrue('Type2' in ds.types())

    def test_get_reference_type(self):
        ds = DataStore('testing/data/reference_types')
        mt1 = ds.get_type('Type1')
        self.assertEqual('testing.reference_types.Type1', mt1.name)
        self.assertEqual('Type1', mt1.ref_type)
        mt2 = ds.get_type('Type2')
        self.assertEqual('testing.reference_types.Type2', mt2.name)
        self.assertEqual('Type2', mt2.ref_type)
        with self.assertRaises(NotAManagedType):
            ds.get_type('XXX')
            
    def test_get_references(self):
        ds = DataStore('testing/data/reference_types')
        with self.assertRaises(NotAManagedType):
            ds.type('XXX')
        references = ds.type('Type1')
        self.assertTrue(hasattr(references, 'get'), 'References does not include a get attribute')
        self.assertTrue(callable(getattr(references, 'get')), 'References.get is not callable')
        self.assertTrue(hasattr(references, 'add'), 'References does not include a add attribute')
        self.assertTrue(callable(getattr(references, 'add')), 'References.add is not callable')
        self.assertTrue(hasattr(references, 'update'), 'References does not include a update attribute')
        self.assertTrue(callable(getattr(references, 'update')), 'References.update is not callable')
        self.assertTrue(hasattr(references, 'filter'), 'References does not include a filter attribute')
        self.assertTrue(callable(getattr(references, 'filter')), 'References.filter is not callable')
        self.assertTrue(hasattr(references, 'delete'), 'References does not include a delete attribute')
        self.assertTrue(callable(getattr(references, 'delete')), 'References.delete is not callable')

    def test_get_reference(self):
        ds = DataStore('testing/data/reference_types')
        refs = ds.type('Type1')
        type1 = refs.get('1')
        self.assertIsNotNone(type1)
        self.assertEqual('1', type1.ref)
        self.assertEqual('Item_1', type1.name)
        self.assertEqual('Item 1', type1.description)

        type1 = refs.get(name='Item_1')
        self.assertIsNotNone(type1)
        self.assertEqual('1', type1.ref)
        self.assertEqual('Item_1', type1.name)
        self.assertEqual('Item 1', type1.description)
        
        typeA = ds.type('Type2').get('A')
        self.assertEqual('A', typeA.ref)
        self.assertEqual('Item_A', typeA.name)
        self.assertEqual('Item A', typeA.description)

    def test_get_reference_raises_DoesNotExist(self):
        ds = DataStore('testing/data/reference_types')
        with self.assertRaises(Type1.DoesNotExist):
            x = ds.type('Type1').get('X')
        with self.assertRaises(Type1.DoesNotExist):
            x = ds.type('Type1').get(name='XXX')

    def test_add_reference_raises_DuplicateReference(self):
        ds = DataStore('testing/data/reference_types')
        type1 = ds.type('Type1').get("1")
        with self.assertRaises(Type1.DuplicateReference):
            x = ds.type('Type1').add(type1)
        with self.assertRaises(Type1.DuplicateReference):
            x = ds.type('Type1').add({}, ref="1")

    def test_update_reference_raises_DoesNotExist(self):
        ds = DataStore('testing/data/reference_types')
        typex = Type1(ref='X', name='Type_X', desc='Type X')
        with self.assertRaises(Type1.DoesNotExist):
            x = ds.type('Type1').update(typex)
        with self.assertRaises(Type1.DoesNotExist):
            x = ds.type('Type1').update({}, ref="X")

    def test_delete_reference_raises_DoesNotExist(self):
        ds = DataStore('testing/data/reference_types')
        typex = Type1(ref='X', name='Type_X', desc='Type X')
        with self.assertRaises(Type1.DoesNotExist):
            x = ds.type('Type1').delete(typex)
        with self.assertRaises(Type1.DoesNotExist):
            x = ds.type('Type1').delete({}, ref="X")
            
    def test_add_update_delete(self):
        if os.path.exists('testing/data/reference_types/Type1/X.json'):
            os.remove('testing/data/reference_types/Type1/X.json')
        ds = DataStore('testing/data/reference_types')
        typex = Type1(ref='X', name='Type_X', desc='Type X')
        self.assertFalse(os.path.exists('testing/data/reference_types/Type1/X.json'))
        ds.type('Type1').add(typex)
        self.assertTrue(os.path.exists('testing/data/reference_types/Type1/X.json'))
        ds = DataStore('testing/data/reference_types')
        added = ds.type('Type1').get('X')
        self.assertEqual(typex, added)
        added.name = 'UPDATED'
        ds.type('Type1').update(added)
        ds = DataStore('testing/data/reference_types')
        updated = ds.type('Type1').get('X')
        self.assertEqual(added, updated)
        self.assertTrue(os.path.exists('testing/data/reference_types/Type1/X.json'))
        ds.type('Type1').delete(updated)
        self.assertFalse(os.path.exists('testing/data/reference_types/Type1/X.json'))
        with self.assertRaises(Type1.DoesNotExist):
            x = ds.type('Type1').get('X')
            
    def test_filter_reference(self):
        ds = DataStore('testing/data/reference_types')
        results = ds.type('Type1').filter(name='Item_1')
        self.assertEqual(1, len(results))
        self.assertEqual('1', results[0].ref)
        self.assertEqual('Item_1', results[0].name)
        self.assertEqual('Item 1', results[0].description)
        
        











       