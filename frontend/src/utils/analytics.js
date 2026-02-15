// Google Analytics 4 Tracking Helper
// Usage: import { trackEvent, trackPageView } from '@/utils/analytics'

export const GA_MEASUREMENT_ID = 'G-XXXXXXXXXX' // Replace with real ID

// Initialize Google Analytics
export function initializeAnalytics() {
    if (typeof window === 'undefined') return

    // Load gtag script
    const script = document.createElement('script')
    script.async = true
    script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`
    document.head.appendChild(script)

    // Initialize dataLayer
    window.dataLayer = window.dataLayer || []
    function gtag() {
        window.dataLayer.push(arguments)
    }
    gtag('js', new Date())
    gtag('config', GA_MEASUREMENT_ID, {
        send_page_view: false // Manual page tracking
    })

    window.gtag = gtag
}

// Track page views
export function trackPageView(pagePath, pageTitle) {
    if (typeof window.gtag === 'undefined') return

    window.gtag('event', 'page_view', {
        page_path: pagePath,
        page_title: pageTitle
    })
}

// Track custom events
export function trackEvent(eventName, parameters = {}) {
    if (typeof window.gtag === 'undefined') return

    window.gtag('event', eventName, parameters)
}

// Predefined event tracking functions
export const analytics = {
    // PPDB Events
    trackPPDBView() {
        trackEvent('ppdb_page_view', {
            event_category: 'PPDB',
            event_label: 'PPDB Landing Page'
        })
    },

    trackPPDBFormStart() {
        trackEvent('ppdb_form_start', {
            event_category: 'PPDB',
            event_label: 'Registration Form Started'
        })
    },

    trackPPDBFormStep(step) {
        trackEvent('ppdb_form_step', {
            event_category: 'PPDB',
            event_label: `Step ${step}`,
            value: step
        })
    },

    trackPPDBFormSubmit(registrationNumber) {
        trackEvent('ppdb_form_submit', {
            event_category: 'PPDB',
            event_label: 'Registration Completed',
            registration_number: registrationNumber
        })
    },

    // Gallery Events
    trackGalleryView(category) {
        trackEvent('gallery_view', {
            event_category: 'Gallery',
            event_label: `Category: ${category}`
        })
    },

    trackGalleryImageClick(imageTitle) {
        trackEvent('gallery_image_click', {
            event_category: 'Gallery',
            event_label: imageTitle
        })
    },

    // Social Share Events
    trackSocialShare(platform, url) {
        trackEvent('social_share', {
            event_category: 'Social',
            event_label: platform,
            url: url
        })
    },

    // WhatsApp Events
    trackWhatsAppClick() {
        trackEvent('whatsapp_click', {
            event_category: 'Contact',
            event_label: 'WhatsApp Button'
        })
    },

    // FAQ Events
    trackFAQView(category) {
        trackEvent('faq_view', {
            event_category: 'FAQ',
            event_label: `Category: ${category}`
        })
    },

    trackFAQExpand(question) {
        trackEvent('faq_expand', {
            event_category: 'FAQ',
            event_label: question
        })
    },

    // Alumni Events
    trackAlumniView() {
        trackEvent('alumni_view', {
            event_category: 'Alumni',
            event_label: 'Alumni Page View'
        })
    },

    trackAlumniLinkedInClick(name) {
        trackEvent('alumni_linkedin_click', {
            event_category: 'Alumni',
            event_label: name
        })
    },

    // Chat Events
    trackChatMessageSent(messageLength) {
        trackEvent('chat_message_sent', {
            event_category: 'Chat',
            event_label: 'AI Chat',
            value: messageLength
        })
    },

    trackChatSessionStart() {
        trackEvent('chat_session_start', {
            event_category: 'Chat',
            event_label: 'New Chat Session'
        })
    },

    // Download Events
    trackDownload(fileName) {
        trackEvent('file_download', {
            event_category: 'Download',
            event_label: fileName
        })
    },

    // Navigation Events
    trackNavigation(destination) {
        trackEvent('navigation', {
            event_category: 'Navigation',
            event_label: destination
        })
    },

    // Search Events
    trackSearch(query) {
        trackEvent('search', {
            event_category: 'Search',
            search_term: query
        })
    }
}

// Export default for convenience
export default {
    init: initializeAnalytics,
    trackPageView,
    trackEvent,
    ...analytics
}
