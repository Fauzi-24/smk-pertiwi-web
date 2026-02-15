import { createI18n } from 'vue-i18n'
import id from './locales/id.json'
import en from './locales/en.json'
import de from './locales/de.json'
import ru from './locales/ru.json'
import jp from './locales/jp.json'
import ar from './locales/ar.json'

const i18n = createI18n({
    legacy: false, // Use Composition API mode
    locale: localStorage.getItem('user-locale') || 'id', // Default language
    fallbackLocale: 'en',
    messages: {
        id,
        en,
        de,
        ru,
        jp,
        ar
    }
})

export default i18n
