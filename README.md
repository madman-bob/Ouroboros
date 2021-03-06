# Ouroboros

Ouroboros is an expressive interpreted programming language, for general purpose programming.
It focuses on bringing the power of Lisp, with the familiarity of C-based languages.
If the word "boilerplate" is ever used to describe an Ouroboros program, then I've done something wrong.

Part of the expressiveness comes from Ouroboros having no reserved words.
What, in many languages, are reserved words, are instead in Ouroboros variables.
As such, this gives programmers the ability to create their own custom structures, of similar power.

This gives powerful tools to programmers, so it will be possible for people to write *really* bad code in this language.
That said, it is possible to write really bad code in any language.
As with all powerful tools, it's up to the user not to hurt themselves.

## Expressiveness

### Control structures

For most purposes, the standard control structures suffice.
But every now and again, you need a control structure that doesn't quite fit.
As Ouroboros blocks are just functions, this means you can write your own control structures.

For example:

```
do_twice = f => {
    f();
    f();
};
```

defines a `do_twice` control structure, that runs its block twice.
You can then use it like so:

```
a = 0;

do_twice {
    a = a + 1;
};

print(a);
```

which prints `2`.

### Simplify component communication

Through use of decorators and compile time variables, can write code for multiple systems as though they're just one.

For example, you can define the decorator:

```
ServerSideFunction = path => f => {
    if (IS_SERVER) {
        my_server.serve(path, f);
        return f;
    } else {
        return () => http.get(path);
    };
};
```

and decorate functions like so:

```
get_current_user = ServerSideFunction("/user") {
    # Do stuff with db to get user
};
```

Then the server-side code presents the `/user` endpoint, and when `get_current_user` is called, it calls the database directly.
Meanwhile, in the client-side code, this function instead makes a HTTP GET call to that same endpoint.

This is similar to the Javascript idea of "isomorphic code".

Further, there is no need to restrict ourselves to a client-server relationship.
We could write code for an arbitrary number of components, as though they were all on the same machine.

### Pass arguments into a function when you can

Currying allows you to give some arguments of a function now, and some of them later.
You can use this to create a collection of similar functions, by passing in some sort of configuration argument.

For example:

```
wrap_tag = tag_name => contents => {
    return "<" + tag_name + ">" + contents + "</" + tag_name + ">";
};

wrap_js = wrap_tag("script");
wrap_css = wrap_tag("style");

print(wrap_js("console.log('Hello, console')"));
print(wrap_js("document.body.innerText = 'Hello, world'"));
print(wrap_css("body { background-color: blue }"));
```

prints

```
<script>console.log('Hello, console')</script>
<script>document.body.innerText = 'Hello, world'</script>
<style>body { background-color: blue }</style>
```

This code defines the `wrap_js` and `wrap_css` functions by passing one of the arguments to `wrap_tag`, and allowing the others to be passed in later.
Then you can use these functions, instead of repeatedly writing `wrap_tag("script", ...)`.

The above is equivalent to

```
wrap_tag = (tag_name, content) => {
    return "<" + tag_name + ">" + contents + "</" + tag_name + ">";
};

wrap_js = content => {
    return wrap_tag("script", content);
};
wrap_css = content => {
    return wrap_tag("style", content);
};
```

but with less boilerplate, and more robust.
If you want to extend `wrap_tag` to take more arguments, then the curried form allows you to do so easily, while the non-curried form requires you update both `wrap_js`, and `wrap_css` as well.

### Change the syntax

Don't like the default name for assignment?
As there are no reserved words, you can assign anything you want to another variable name.

For example:

```
equals = =;

hello equals "Hello";
say equals print;

say hello;
```

will indeed print `Hello`.

This allows you to warp the language to whatever your specific use-case may be.

Naturally, this will increase onboarding time for new programmers in your codebase.
But these sorts of domain specific issues would otherwise be encoded in functions, and objects.
As they'll exist, anyway, it's better to bring them out into the open.

## Design principles

### No keywords

By assigning special meaning to certain symbols, we admit that our language is not powerful enough to express those concepts within itself.
As such, there are no special words in Ouroboros, and the process of working out how to include those ideas makes the language more powerful.

For example, there is no special notations for functions.
It's just another form of assignment.

```
some_variable = 1;
some_function = {
    print "Hi";
};
```

Another consequence of this is that loops are just another sort of statement, and so need a semicolon after them.

```
i = 0;
while (i < 10) {
    print i;
    i = i + 1;
};
```

### Don't forbid for the sake of forbidding

An expression being strange, or useless, is not same as it being invalid.
Just because *I* can't think of how it might be used, doesn't mean it can't be.

As an extreme example, once upon a time, the identity function was seen as useless.
"Why would you call a function that does nothing? Just don't call it in the first place."
But with various functional ideas becoming more popular, the identity function starts becoming useful all over the place.

### Abstract as much as possible

The purpose of a programming language is to allow a programmer to describe, to a computer, what they want doing.
By keeping things as abstract as possible, we allow programmers to use them in precisely the way they need.

As another benefit, the process of abstraction may reveal unexpected similarities, which can then be exploited to provide new tools in the programmers kit.
For example, much of functional programming comes from the recognition that we can use functions just as we would any other variable.

## Technical ideas

Some technical ideas of language features to come:

### Able to iterate over statements in a function

For ease of compiling/meta-programming.

### Equality of functions

Two functions `f`, and `g` are considered equal (`f == g`) if they are defined at the same point in the source code, and their containing scopes are equal.
Scopes are equal if the functions creating them are equal, and all of their variables are equal.

I've considered having `f == g` if they are
[alpha equivalent](https://en.wikipedia.org/wiki/Lambda_calculus#Alpha_equivalence),
but decided against it, as two functions may be alpha equivalent, but not
[semantically equivalent](https://en.wikipedia.org/wiki/Semantic_equivalence).

eg. The constructors

```
person = (name, age) => { ... };
company = (name, age) => { ... };
```

may happen to be alpha equivalent, but they represent different objects.

### Ability to modify the syntax from within the language

Bit of a long-term goal.
Not thought too much about this, yet.

Ideally, I want to be able to completely rewrite the syntax of the language from within itself.
To demonstrate this, I'd like to be able to start with something C-like, and end up with
[Brainfuck](https://en.wikipedia.org/wiki/Brainfuck)

## Setup

Ensure Python is installed.
Ouroboros is developed in Python 3.6, but may work in other versions.
Then run

    pip install -r requirements.txt

## Usage

Ouroboros is currently written as an interpreter, in Python.

    python -m ouroboros [-h] [file]

## Examples

Look in the [`examples`](examples) directory for a number of examples.
