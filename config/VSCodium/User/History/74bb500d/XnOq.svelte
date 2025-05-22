<script>
    import { Button } from '$lib/components/ui/button';
    import { Input } from '$lib/components/ui/input';
    import { Label } from '$lib/components/ui/label';
    import { goto } from '$app/navigation';
    import { supabase } from '$lib/supabase';
    import { user } from '$lib/stores/authStore';
    import { onMount } from 'svelte';
    import googleUrl from "$lib/assets/google.svg"
    import logoUrl from "$lib/assets/logow.svg"

    let email = '';
    let password = '';
    let loading = false;
    let error = null;
  
    onMount(() => {
      if ($user) {
        goto('/dashboard');
      }
    });
  
    async function handleLogin() {
      if (!email || !password) {
        error = 'Please enter both email and password';
        return;
      }
  
      try {
        loading = true;
        error = null;
        const { data, error: authError } = await supabase.auth.signInWithPassword({
          email,
          password
        });
  
        if (authError) throw authError;
        
        if (data?.user) {
          user.set(data.user);
          goto('/dashboard');
        }
      } catch (err) {
        console.error('Error logging in:', err);
        error = err.message || 'Failed to login. Please try again.';
      } finally {
        loading = false;
      }
    }
  
    async function handleGoogleLogin() {
      try {
        loading = true;
        error = null;
        const { error: authError } = await supabase.auth.signInWithOAuth({
          provider: 'google',
          options: {
            redirectTo: 'https://resumix.ru' // Or your desired redirect URL
          }
        });
  
        if (authError) throw authError;
  
      } catch (err) {
        console.error('Error during Google login:', err);
        error = err.message || 'Failed to sign in with Google. Please try again.';
      } finally {
        loading = false;
      }
    }
  </script>
  
  <div class="flex min-h-screen bg-gray-950 text-gray-100">
    <div class="flex-1 flex items-center justify-center">
      <div class="w-full max-w-md p-8 space-y-8 bg-gray-900 rounded-lg shadow-xl border border-gray-800">
        <div class="text-center">
          <a href="/" class="inline-flex items-center gap-2 mb-6">
            <img src={logoUrl} alt="Logo" width="20" height="20"/>
            <span class="text-xl font-bold">Resumix</span>
          </a>
          <h1 class="text-2xl font-bold">Войти в аккаунт</h1>
          <p class="mt-2 text-gray-400">
            Введите данные, чтобы получить доступ к вашему аккаунту.
          </p>
        </div>
  
        <form on:submit|preventDefault={handleLogin} class="space-y-6">
          {#if error}
            <div class="p-3 bg-destructive/20 border border-destructive text-destructive rounded-md text-sm">
              {error}
            </div>
          {/if}
  
          <div class="space-y-2">
            <Label for="email">Email</Label>
            <Input 
              id="email" 
              type="email" 
              placeholder="your.email@example.com" 
              bind:value={email}
              disabled={loading}
              class="bg-gray-800 border-gray-700 focus:border-primary"
            />
          </div>
  
          <div class="space-y-2">
            <div class="flex items-center justify-between">
              <Label for="password">Password</Label>
            </div>
            <Input 
              id="password" 
              type="password" 
              placeholder="••••••••" 
              bind:value={password}
              disabled={loading}
              class="bg-gray-800 border-gray-700 focus:border-primary"
            />
          </div>
  
          <Button type="submit" class="w-full" disabled={loading}>
            {loading ? 'Накручиваем опыт...' : 'Войти'}
          </Button>
  
          <!-- Google OAuth Button -->
          <Button on:click={handleGoogleLogin} class="w-full bg-white text-black">
            <img src={googleUrl} alt="google icon" class="mr-3">
            Войти через Google
          </Button>
  
          <div class="text-center text-sm">
            Еще нет аккаунта?
            <a href="/register" class="text-indigo-400 hover:underline">
              Зарегистрироваться
            </a>
          </div>
        </form>
  
      </div>
    </div>
  
    <div class="hidden lg:flex lg:flex-1 bg-gray-900">
      <div class="flex flex-col justify-center p-12 bg-gray-950/60 w-full">
        <div class="max-w-md">
          <h2 class="text-3xl font-bold mb-6">Выделяйтесь благодаря индивидуальному резюме для каждого отклика</h2>
          <p class="text-gray-300 mb-8">
            Наша платформа на базе искусственного интеллекта поможет вам настроить свое резюме в соответствии с требованиями вакансии, что повысит ваши шансы попасть на собеседование.
          </p>
          <div class="flex items-center space-x-4">
            <div class="flex -space-x-2">
              <div class="w-8 h-8 rounded-full bg-primary text-black flex items-center justify-center text-xs font-bold">JD</div>
              <div class="w-8 h-8 rounded-full bg-primary/80 text-black flex items-center justify-center text-xs font-bold">MK</div>
              <div class="w-8 h-8 rounded-full bg-primary/60 text-black flex items-center justify-center text-xs font-bold">AS</div>
            </div>
            <p class="text-sm text-gray-300">500+ человек уже обновили свое резюме</p>
          </div>
        </div>
      </div>
    </div>
  </div>
