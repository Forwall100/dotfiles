<script>
    import { Button } from '$lib/components/ui/button';
    import { Input } from '$lib/components/ui/input';
    import { Label } from '$lib/components/ui/label';
    import { goto } from '$app/navigation';
    import { supabase } from '$lib/supabase';
    import { user } from '$lib/stores/authStore';
    import { onMount } from 'svelte';
    import logoUrl from "$lib/assets/logow.svg"
  
    let name = '';
    let email = '';
    let password = '';
    let confirmPassword = '';
    let loading = false;
    let error = null;
  
    onMount(() => {
      if ($user) {
        goto('/dashboard');
      }
    });
  
    async function handleRegister() {
      if (!email || !password || !name) {
        error = 'Please fill in all required fields';
        return;
      }
  
      if (password !== confirmPassword) {
        error = 'Passwords do not match';
        return;
      }
  
      if (password.length < 6) {
        error = 'Password must be at least 6 characters';
        return;
      }
  
      try {
        loading = true;
        error = null;
        
        const { data, error: authError } = await supabase.auth.signUp({
          email,
          password,
          options: {
            data: {
              full_name: name,
            },
            redirectTo: 'https://resumix.ru'
          }
        });
  
        if (authError) throw authError;
        
        if (data?.user) {
          // Create a profile for the user
          const { error: profileError } = await supabase
            .from('profiles')
            .insert([
              { 
                id: data.user.id, 
                full_name: name,
                credits: 3 // Starting credits for new users
              }
            ]);
            
          if (profileError) console.error('Error creating profile:', profileError);
          
          user.set(data.user);
          goto('/confirm-email');
        }
      } catch (err) {
        console.error('Error registering:', err);
        error = err.message || 'Failed to register. Please try again.';
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
            <img src={logoUrl} alt="Logo" width="20" height="20" />
            <span class="text-xl font-bold">Resumix</span>
          </a>
          <h1 class="text-2xl font-bold">Регистрация</h1>
          <p class="mt-2 text-gray-400">
            Начните бесплатно составлять свое резюме
          </p>
        </div>
  
        <form on:submit|preventDefault={handleRegister} class="space-y-6">
          {#if error}
            <div class="p-3 bg-destructive/20 border border-destructive text-destructive rounded-md text-sm">
              {error}
            </div>
          {/if}
  
          <div class="space-y-2">
            <Label for="name">Юзернейм</Label>
            <Input 
              id="name" 
              type="text" 
              placeholder="John Doe" 
              bind:value={name}
              disabled={loading}
              required
              class="bg-gray-800 border-gray-700 focus:border-primary"
            />
          </div>
  
          <div class="space-y-2">
            <Label for="email">Email</Label>
            <Input 
              id="email" 
              type="email" 
              placeholder="your.email@example.com" 
              bind:value={email}
              disabled={loading}
              required
              class="bg-gray-800 border-gray-700 focus:border-primary"
            />
          </div>
  
          <div class="space-y-2">
            <Label for="password">Пароль</Label>
            <Input 
              id="password" 
              type="password" 
              placeholder="••••••••" 
              bind:value={password}
              disabled={loading}
              required
              class="bg-gray-800 border-gray-700 focus:border-primary"
            />
            <p class="text-xs text-gray-400">Must be at least 6 characters</p>
          </div>
  
          <div class="space-y-2">
            <Label for="confirmPassword">Потдвержение пароля</Label>
            <Input 
              id="confirmPassword" 
              type="password" 
              placeholder="••••••••" 
              bind:value={confirmPassword}
              disabled={loading}
              required
              class="bg-gray-800 border-gray-700 focus:border-primary"
            />
          </div>
  
          <Button type="submit" class="w-full" disabled={loading}>
            {loading ? 'Накручиваем опыт...' : 'Зарегистрироваться'}
          </Button>
  
          <!-- Google OAuth Button -->
          <Button on:click={handleGoogleLogin} class="w-full bg-blue-600 hover:bg-blue-700 text-white">
            Войти через Google
          </Button>
  
          <div class="text-center text-sm">
            Уже есть аккаунт?
            <a href="/login" class="text-indigo-400 hover:underline">
              Войти
            </a>
          </div>
        </form>
  
        
      </div>
    </div>
  
    <div class="hidden lg:flex lg:flex-1 bg-gray-900">
      <div class="flex flex-col justify-center p-12 bg-gray-950/60 w-full">
        <div class="max-w-md">
          <h2 class="text-3xl font-bold mb-6">Создайте бесплатный аккаунт, чтобы начать получать приглашения на собесы. </h2>
          <p class="text-gray-300 mb-8">
            Благодаря резюме, оптимизированным с помощью AI, вы сможете быстрее получить работу 
          </p>
          <div class="flex flex-col space-y-4">
            <div class="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-primary mr-2">
                <polyline points="20 6 9 17 4 12" />
              </svg>
              <span>Бесплатный редактор резюме</span>
            </div>
            <div class="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-primary mr-2">
                <polyline points="20 6 9 17 4 12" />
              </svg>
              <span>Множество бесплатных шаблонов</span>
            </div>
            <div class="flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="text-primary mr-2">
                <polyline points="20 6 9 17 4 12" />
              </svg>
              <span>Не нужна привязка карты</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
