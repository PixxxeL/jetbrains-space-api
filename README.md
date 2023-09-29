# API к Space

Частичное прокси к API системы Space от JetBrains. Делалось под определенные нужды, так что здесь не всё, но можно подсмотреть принципы и дальше дописать сасому.

## Пример использования

```python
from space import SpaceApi

# вместо example должно быть название вашей организации
# токен нужно получить в личном кабинете JetBrains
api = SpaceApi('https://example.jetbrains.space', 'xxx')
print(api.get_projects())
```

Токен можно получить в `https://example.jetbrains.space/extensions` (вместо `example` - ваша организация):

* Добавляете приложение
* В авторизации добавляете разрешения
* Добавляете permanent token
