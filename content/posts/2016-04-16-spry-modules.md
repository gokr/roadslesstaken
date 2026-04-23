---
title: Spry Modules
date: '2016-04-16'
slug: spry-modules
categories:
- Spry
- Ni
- Smalltalk
- Homoiconic
- Languages
- Programming
---
As discussed in [the previous article](http://goran.krampe.se/2016/04/09/spry-image-model/) I want Spry to have a trivially accessible persistence mechanism enabling something similar to the **Smalltalk image model**, but based on a database. The memory organisation in Spry is basically nested Maps. After dwelling a bit on the inevitable hard question about **modules and namespaces** I have decided on a design that I hope will turn out simple and reasonably powerful!

![Modules](/spry/modules.jpg){ style="float:right; margin:0 0 1em 1em;"}

Smalltalk has a Dictionary holding all the globals forming "the roots" of the object memory. In Smalltalk this Dictionary is also itself a global variable accessible as `Smalltalk`, in other words `Smalltalk == (Smalltalk at: #Smalltalk)`. The primary use of `Smalltalk` is to hold all classes by name, so they are all reachable as globals. Obviously `Smalltalk` can also hold any kind of object (not just classes) as a global.

Spry also has such a top level Dictionary, but in Spry we call a Dictionary a `Map` to be a little bit more aligned in terminology with other languages (and it's shorter). This top level Map is the `root` Map and it is accessible via the word `root`. In Spry the `root` word is actually bound to a primitive function returning this `Map`, so in Spry we also have `root == (root at: 'root)`.

Ok, so Spry has a `Map` of globals and one way of using Spry is simply by populating `root` with words bound to functions making these functions globally accessible, it's how I have done it so far. Yeah, yeah, I know, but for smaller systems it probably works just fine!

But...
<!--more-->

## Modules
But we **do** want a Module concept and given that I once designed a Namespace model for Squeak (that never was accepted) - it was inevitable I guess that it would reappear in Spry! :)

As many other languages do, I also simplify by making a "Module" do double duty as a "Namespace". It's a reasonable approximation although to be precise a Module is normally a deployment, versioning and distribution unit and a Namespace should ideally be aligned with how we humans are organised, but... whatever. In Spry I also simplify by **not allowing nesting of Modules**. A Module is simply a `Map` bound to a global word.

Modules need to have meta information about them. In Nim we use a `Foo.nimble` file to contain this meta information. In the JavaScript world there is a `package.json` file containing meta information. In Spry, since a Module is a `Map`, we let the `_meta` key hold a Map of meta information:

```
_meta = {
  name = "Foo"
  version = "1.0"
  author = "Göran Krampe"
}
```

The name of the Module is thus only kept as meta information, this means that the code loading the module into our system decides what the Module should **actually** be named - thus we can choose to load a Module `Foo` by the name `Foo2` if we already have a Module called `Foo` in the system. It could for example be used to have two different versions of the same Module loaded at the same time.

So how do we refer to things in different Modules? Obviously we can do it manually using `(root at: 'Network) at: 'Socket`, it's just a global `Map` after all, but `Network at: 'Socket` is simpler. I am also introducing yet another word type - a **Module qualified word**. It would look like `Network::Socket` and be evaluated as `Network at: 'Socket`. If we load another `Foo` as `Foo2`, then all existing references like `Foo::Cat` will of course not refer to the new `Foo2`, but we could easily scan for them and modify them, if we so wish.

## To import... or not!

Finally, we face the issue of **imports**. Almost all programming languages use imports, often per class or file, but also per module. It's worth recognizing what **true purpose** they actually serve.

![Autoimport](/spry/autoimport.jpg){ style="float:right; margin:0 0 1em 1em;"}

1. One use of them is to avoid typing long names in the actual code, but ... that would typically only be an issue if module names where.. say **very long** like `com.MyCoolCompany.ProjectX.Base.Common`, but they aren't in Spry, since we don't allow nesting nor do we want people to use Internet domain names like that.

2. It can be used to constrain the allowed references a Module can have, but... in my experience it's not often used to do that. One could however imagine a system of declarative rules of what modules can access what other module, or which group of modules can depend on which other group. In fact, I designed such a tool for Java back in ... waaay back.

3. To enhance completion, only completing within the imported union of modules. I don't really view this as a critical thing, and it can also be solved using heuristics. Smalltalk systems also complete these days, and not having imports hasn't really made it less useful.

4. To act as documentation for a Module showing what other Modules it uses, but... then we should not allow fully qualified references in the code since that invalidates this purpose. And we could trivially scan and find all usages within the Module without the import statements.


## To sum it up...

![No](/spry/noimports.jpg){ style="display:block; margin:0 auto;"}

In my proposal for Squeak there were no imports either, the idea was to always have the full reference in the source code, but to let browsers "render them short" if the unqualified name still was unique in the image. In Spry I am opting for a slightly different approach:

* For a **regular word** lookup eventually ends up looking in `root` for globals. If it fails, it looks through the Modules one by one until it finds a hit. This means `Socket` will resolve to `Network::Socket` if `Network` is the first module found containing that word, and there is no global `Socket` shadowing it.
* For a **module qualified word**, like `Network::Socket`, lookup is directly in the module by that name, we never look at globals. If there is no hit, it's not resolved, so no need to look elsewhere.

This means we can still use `Socket` in short form, but be aware that it means _"Give me the first thing you find called Socket"_. If we qualify it means _"Give me Socket in the Network module"_.

Thus, if we let `root at: 'modules` be a Block of the modules that wish to participate in such an ordered lookup - that should be enough!

## Next Steps

So I will:

* Write some module tests.
* Add the global modules block and adjust lookup to use it for non qualified words.
* Add the module qualified word and it's special lookup.
* Make some base modules and add some mechanisms to `ispry` (the REPL) to use them.

When this works it's getting time to hook into [Sophia](https://github.com/gokr/nim-sophia)!

Happy Sprying!

