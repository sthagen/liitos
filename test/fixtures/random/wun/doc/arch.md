# Architecture

The top level plan in use for building the best software ever.

Blueprints may link to visuals like \ref{fig:blue-square} and link to them.

![Blue Square](images/blue.png "Blue Square 32x32 \label{fig:blue-square}"){width=98% height=98%}

In some cases backward references to figures like \ref{fig:blue-square} are in use.

It is not always possible to stop organizations from creating deeply nested matrioshka like section trees.

Let us test how this passes the publication or rendering pipeline. 

## Why Not?

Second level heading results in a subsection under our regime.

### This is OK

Third level results in subsubsection.

#### Is this really useful?

Laying out a level four heading should end in a paragraph.

##### Until the Cows Come Home

Overengineering is so much fun.

###### This is not Funny for Anyone

Who knows where we are in the tree and if we evver see the light of the sun again ...

## Lists Maybe?

Unordered, nested, and tight?

- wun
  - wunder
- two
- three
  - hree
    - ree
      - re
        - e
- four

Ordered and tight:

1. uno
1. due
1. tre


And a fenced code block:

```cpp
int main(){}
```

This is all we write about the architecture.

Wait, mermaids!

```{.mermaid background=transparent format=png loc=images filename=alice-and-john caption="Alice and John - Relationship as a Sequence" width=1200}
sequenceDiagram
    Alice->>John: Hello John, how are you?
    John-->>Alice: Great!
```

The auto-generated label should make the reference work like so: \ref{fig:alice-and-john}. Does it?
