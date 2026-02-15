import { createRouter, createWebHistory } from 'vue-router'
import MainLayout from '../layouts/MainLayout.vue'

// Lazy load views for better performance
const Home = () => import('../views/Home.vue')
const Profil = () => import('../views/Profil.vue')
const Jurusan = () => import('../views/Jurusan.vue')
const Guru = () => import('../views/Guru.vue')
const Galeri = () => import('../views/Galeri.vue')
const Kontak = () => import('../views/Kontak.vue')
const PPDB = () => import('../views/PPDB.vue')
const Berita = () => import('../views/Berita.vue')
const Chat = () => import('../views/Chat.vue')

const routes = [
    {
        path: '/',
        component: MainLayout,
        children: [
            {
                path: '',
                name: 'Home',
                component: Home,
                meta: { title: 'Beranda' }
            },
            {
                path: 'profil',
                name: 'Profil',
                component: Profil,
                meta: { title: 'Profil Sekolah' }
            },
            {
                path: 'jurusan',
                name: 'Jurusan',
                component: Jurusan,
                meta: { title: 'Kompetensi Keahlian' }
            },
            {
                path: 'guru',
                name: 'Guru',
                component: Guru,
                meta: { title: 'Dewan Guru' }
            },
            {
                path: 'galeri',
                name: 'Galeri',
                component: Galeri,
                meta: { title: 'Galeri Kegiatan' }
            },
            {
                path: 'kontak',
                name: 'Kontak',
                component: Kontak,
                meta: { title: 'Hubungi Kami' }
            },
            {
                path: 'ppdb',
                name: 'PPDB',
                component: PPDB
            },
            {
                path: 'ppdb/daftar',
                name: 'PPDBForm',
                component: () => import('../views/PPDBForm.vue')
            },
            {
                path: 'berita',
                name: 'Berita',
                component: Berita
            },
            {
                path: 'faq',
                name: 'FAQ',
                component: () => import('../views/FAQ.vue')
            },
            {
                path: 'alumni',
                name: 'Alumni',
                component: () => import('../views/Alumni.vue')
            },
            {
                path: 'chat',
                name: 'Chat',
                component: Chat
            }
        ]
    },
    {
        path: '/admin/login',
        name: 'AdminLogin',
        component: () => import('../views/AdminLogin.vue')
    },
    {
        path: '/admin/dashboard',
        name: 'AdminDashboard',
        component: () => import('../views/AdminDashboard.vue'),
        meta: { requiresAuth: true }
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: () => import('../views/NotFound.vue')
    }
]

const router = createRouter({
    history: createWebHistory(),
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition
        }
        return { top: 0, behavior: 'smooth' }
    },
    routes
})

// Global Navigation Guard (Title + Auth)
router.beforeEach((to, from, next) => {
    // 1. Update Document Title
    const defaultTitle = 'SMK Pertiwi Kuningan'
    document.title = to.meta.title ? `${to.meta.title} | ${defaultTitle}` : defaultTitle

    // 2. Check Authentication
    if (to.matched.some(record => record.meta.requiresAuth)) {
        const token = localStorage.getItem('admin_token')
        // Start loading bar (mock implementation via window event or state)
        if (typeof window !== 'undefined') {
            window.dispatchEvent(new Event('start-loading'))
        }
        if (!token) {
            next({ name: 'AdminLogin' })
            return
        }
    }

    // 3. Proceed
    next()
})

router.afterEach(() => {
    if (typeof window !== 'undefined') {
        window.dispatchEvent(new Event('stop-loading'))
    }
})

export default router
