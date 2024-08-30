```mermaid
classDiagram
FileDao <|-- ListFileDao
FileDao <|-- DictFileDao
class FileDao{
 -fileSystem : IFileSystem
 +FileDao(fileSystem : IFileSystem) FileDao
 +FileDao() FileDao
 +LoadFile(file : string) FileDto
}
class ListFileDao{
 +name
}
class DictFileDao{
 +name
}
```
