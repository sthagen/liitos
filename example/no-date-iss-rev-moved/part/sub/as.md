## As

Sub part As with again includes.

```{.python .cb.run}
with open('as1.md') as fp:
    print(fp.read())
```

## Asb

Funny image reference from upstream: 

![Caption for dot dot images in blue](../images/blue.png) <!-- no alt text ... and a comment eol -->

The parser survives the comment but:

>the caption "Caption for dot dot images in blue" will get lost 
>because pandoc does not place the image in a figure environment

End of sub part cascade.
