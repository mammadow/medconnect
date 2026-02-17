import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('../views/Home.vue')
    },
    {
      path: '/about',
      name: 'about',
      component: () => import('../views/About.vue')
    },
    {
      path: '/contact',
      name: 'contact',
      component: () => import('../views/Contact.vue')
    },
    {
      path: '/login',
      name: 'login',
      component: () => import('../views/Login.vue'),
      meta: { guest: true }
    },
    {
      path: '/register',
      name: 'register',
      component: () => import('../views/Register.vue'),
      meta: { guest: true }
    },
    {
      path: '/doctor/dashboard',
      name: 'doctor-dashboard',
      component: () => import('../views/doctor/Dashboard.vue'),
      meta: { requiresAuth: true, role: 'doctor' }
    },
    {
      path: '/doctor/prescriptions/create',
      name: 'create-prescription',
      component: () => import('../views/doctor/CreatePrescription.vue'),
      meta: { requiresAuth: true, role: 'doctor' }
    },
    {
      path: '/patient/dashboard',
      name: 'patient-dashboard',
      component: () => import('../views/patient/Dashboard.vue'),
      meta: { requiresAuth: true, role: 'patient' }
    },
    {
      path: '/patient/prescriptions',
      name: 'patient-prescriptions',
      component: () => import('../views/patient/Prescriptions.vue'),
      meta: { requiresAuth: true, role: 'patient' }
    },
    {
      path: '/patient/orders',
      name: 'patient-orders',
      component: () => import('../views/patient/Orders.vue'),
      meta: { requiresAuth: true, role: 'patient' }
    },
    {
      path: '/profile',
      name: 'profile',
      component: () => import('../views/Profile.vue'),
      meta: { requiresAuth: true }
    },
    {
      path: '/chemist/dashboard',
      name: 'chemist-dashboard',
      component: () => import('../views/chemist/Dashboard.vue'),
      meta: { requiresAuth: true, role: 'chemist' }
    },
    {
      path: '/chemist/orders',
      name: 'chemist-orders',
      component: () => import('../views/chemist/Orders.vue'),
      meta: { requiresAuth: true, role: 'chemist' }
    },
    {
      path: '/admin',
      name: 'admin-login',
      component: () => import('../views/admin/Login.vue'),
      meta: { guest: true }
    },
    {
      path: '/admin/dashboard',
      name: 'admin-dashboard',
      component: () => import('../views/admin/Dashboard.vue'),
      meta: { requiresAuth: true, role: 'admin' }
    }
  ]
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    if (to.meta.role === 'admin') {
      next('/admin')
    } else {
      next('/login')
    }
  } else if (to.meta.guest && authStore.isAuthenticated) {
    // Redirect authenticated users based on their role
    if (authStore.user.role === 'doctor') {
      next('/doctor/dashboard')
    } else if (authStore.user.role === 'patient') {
      next('/patient/dashboard')
    } else if (authStore.user.role === 'chemist') {
      next('/chemist/dashboard')
    } else if (authStore.user.role === 'admin') {
      next('/admin/dashboard')
    }
  } else if (to.meta.role && authStore.user.role !== to.meta.role) {
    // Prevent users from accessing routes for different roles
    next('/')
  } else {
    next()
  }
})

export default router
