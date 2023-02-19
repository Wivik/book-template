# Contribute

## See something wrong ?

Open an issue in the repository with the problem and the fix to apply. Any helpful contributions are appreciated !

If you want to directly fix the book's content, see below :

## Want to develop the content ?

### How this repository's organized

The book sources are in the `book` directory.

The pages starting by `00-*.md` are the title, cover, preface, etc.

The book content starts with the `01-*.md` files. One file per chapter.

The `diagram` directory contains the sources of the illustrations.

The `img` directory contains the images included in the book.

### How to add or modify content

Fork the repository.

Propose your changes with a pull request.

Add yourself in the Contributors page of the book if it's the first time.

### Diagrams conventions

The diagrams are made with [Excalidraw](https://excalidraw.com/) using the following convention :

- A background frame filled with `#ced4da`
- Grouped items's background is `#868e96`
- When the diagram represents a decision workflow, the follow colors are used :
	+ `#868e96` for the first steps
	+ `#fd7e14`for the question steps
	+ `#fa5252` for the error steps
	+ `#40c057` for the success steps
- Ensure you name the arrows to ensure the colors may not confuse for black and white e-reading devices

### Image insertion convention

Each image must be described since this text will be displayed above them. Use the expected markdown convention :

```markdown
![This is a description](./img/image.png)
```

