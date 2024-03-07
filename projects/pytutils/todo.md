
Catalogs are added with a tag
=============================

Store catalog lists in a {tag/namespace: [catA, catB]}

Di instance has a tag/namespace that's set dynamically.

"Adding" a catalog simply adds with the tag/namespace argument as the key.

Catalog order always returns the current di tag/namespace list iterator.


Catalogs are added and removed from di instance
===============================================

Each provide their own providers, and the ordering can be specified.
Di instance when providing goes through the catalogs list looking for the first provider that provides said name.
Since instances are stored in the provider itself, this allows easy add/remove of catalogs live, which simplifies testing.


Simplify injection API
======================

Create objects for each kind of injection, ie:
- ArgInjection(key, name=None)
- KwargInjection(key, name=None)
- ClassPropertyInjection(key, name=None)
- PropertyInjection(key, name=None) -- Instance level property

Utilize these internally:
>>> di.inject('key1', 'key2', name3='key3')
Would get turned into
>>> di.inject(ArgInjection('key1'), ArgInjection('key2'), KwargInjection('key3', name='name3'))

You could inject a classproperty via:
>>> di.inject(ClassPropertyInjection('key1'))


Simplify catalog provider API, merge with register_factory
==========================================================

Currently you create a Provider object via provide(), but this could just set properties on the decorated, marking it as a provider instead of converting it into one.

This would allow register_factory to be the same API used on catalogs as well.


Abstract base catalogs
======================

Provide a way to specify what providers must be added to the Di instance.

If it's not, at a certain call point, perhaps manually done to specify that you're done loading catalogs or want to check if all needed is loaded.
